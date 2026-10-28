<?php
/*
 * EQUESTRIAN MEDIA — send-mail.php
 * Receives the contact form (js/bundle.js posts it with fetch) and delivers it
 * through the mailbox's own SMTP server. Settings live in mail-config.php.
 * Responds with JSON; any non-2xx status makes the form show its error line.
 */

declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');

function respond(int $status, array $body): void
{
    http_response_code($status);
    echo json_encode($body);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Allow: POST');
    respond(405, ['ok' => false, 'error' => 'Method not allowed']);
}

// Honeypot: real visitors never see or fill this field, bots usually do.
// Pretend success so the bot learns nothing.
if (trim((string)($_POST['_gotcha'] ?? '')) !== '') {
    respond(200, ['ok' => true]);
}

$configFile = __DIR__ . '/mail-config.php';
if (!is_file($configFile)) {
    error_log('send-mail.php: mail-config.php is missing');
    respond(500, ['ok' => false, 'error' => 'Mail is not configured']);
}
$config = require $configFile;

/** Single-line field: trims, strips control characters (blocks header injection), caps length. */
function clean_line(string $value, int $max): string
{
    $value = preg_replace('/[\x00-\x1F\x7F]+/u', ' ', $value) ?? '';
    return mb_substr(trim($value), 0, $max);
}

$name    = clean_line((string)($_POST['name'] ?? ''), 120);
$email   = clean_line((string)($_POST['email'] ?? ''), 160);
$phone   = clean_line((string)($_POST['phone'] ?? ''), 30);
$message = mb_substr(trim(str_replace("\0", '', (string)($_POST['message'] ?? ''))), 0, 5000);

$errors = [];
if ($name === '') {
    $errors[] = 'name';
}
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $errors[] = 'email';
}
if (!preg_match('/^[0-9+()\-\s]{7,20}$/', $phone)) {
    $errors[] = 'phone';
}
if ($errors) {
    respond(422, ['ok' => false, 'error' => 'Invalid fields', 'fields' => $errors]);
}

$subject = 'New campaign brief from equestrianmedia.in — ' . $name;
$body = "New enquiry from the website contact form\n"
      . "------------------------------------------\n\n"
      . "Name:    {$name}\n"
      . "Email:   {$email}\n"
      . "Phone:   {$phone}\n\n"
      . "Message:\n" . ($message !== '' ? $message : '(none)') . "\n\n"
      . "------------------------------------------\n"
      . 'Sent ' . gmdate('D, d M Y H:i') . " UTC from " . ($_SERVER['REMOTE_ADDR'] ?? 'unknown') . "\n";

try {
    smtp_send($config, $config['to_email'], $subject, $body, $email, $name);
} catch (Throwable $e) {
    error_log('send-mail.php: ' . $e->getMessage());
    respond(502, ['ok' => false, 'error' => 'Could not send the message']);
}

respond(200, ['ok' => true]);


/* --------------------------------------------------------------------------
   Minimal SMTP client: SSL (465) or STARTTLS (587), AUTH LOGIN, one recipient.
   -------------------------------------------------------------------------- */

function smtp_send(array $cfg, string $to, string $subject, string $body, string $replyTo, string $replyName): void
{
    $host = (string)$cfg['host'];
    $port = (int)$cfg['port'];
    $enc  = strtolower((string)($cfg['encryption'] ?? 'ssl'));

    $remote = ($enc === 'ssl' ? 'ssl://' : 'tcp://') . $host . ':' . $port;
    $context = stream_context_create(['ssl' => ['peer_name' => $host, 'SNI_enabled' => true]]);
    $sock = @stream_socket_client($remote, $errno, $errstr, 15, STREAM_CLIENT_CONNECT, $context);
    if (!$sock) {
        throw new RuntimeException("Connect to {$remote} failed: {$errstr} ({$errno})");
    }
    stream_set_timeout($sock, 20);

    try {
        smtp_expect($sock, 220);
        $ehloHost = $_SERVER['SERVER_NAME'] ?? 'localhost';
        smtp_cmd($sock, 'EHLO ' . $ehloHost, 250);

        if ($enc === 'tls') {
            smtp_cmd($sock, 'STARTTLS', 220);
            $methods = STREAM_CRYPTO_METHOD_TLSv1_2_CLIENT
                     | (defined('STREAM_CRYPTO_METHOD_TLSv1_3_CLIENT') ? STREAM_CRYPTO_METHOD_TLSv1_3_CLIENT : 0);
            if (!stream_socket_enable_crypto($sock, true, $methods)) {
                throw new RuntimeException('STARTTLS negotiation failed');
            }
            smtp_cmd($sock, 'EHLO ' . $ehloHost, 250);
        }

        smtp_cmd($sock, 'AUTH LOGIN', 334);
        smtp_cmd($sock, base64_encode((string)$cfg['username']), 334);
        smtp_cmd($sock, base64_encode((string)$cfg['password']), 235, true);

        $from = (string)$cfg['from_email'];
        smtp_cmd($sock, "MAIL FROM:<{$from}>", 250);
        smtp_cmd($sock, "RCPT TO:<{$to}>", [250, 251]);
        smtp_cmd($sock, 'DATA', 354);

        $domain = substr(strrchr($from, '@') ?: '@localhost', 1);
        $headers = [
            'Date: ' . date(DATE_RFC2822),
            'From: ' . encode_header((string)($cfg['from_name'] ?? '')) . " <{$from}>",
            "To: <{$to}>",
            'Reply-To: ' . encode_header($replyName) . " <{$replyTo}>",
            'Subject: ' . encode_header($subject),
            'Message-ID: <' . bin2hex(random_bytes(12)) . "@{$domain}>",
            'MIME-Version: 1.0',
            'Content-Type: text/plain; charset=UTF-8',
            'Content-Transfer-Encoding: base64',
        ];
        $data = implode("\r\n", $headers) . "\r\n\r\n"
              . rtrim(chunk_split(base64_encode($body), 76, "\r\n")) . "\r\n.";
        smtp_cmd($sock, $data, 250);

        fwrite($sock, "QUIT\r\n");
    } finally {
        fclose($sock);
    }
}

/** RFC 2047 encode a header value so names and dashes survive any mail client. */
function encode_header(string $value): string
{
    return preg_match('/[^\x20-\x7E]/', $value) ? '=?UTF-8?B?' . base64_encode($value) . '?=' : $value;
}

/** Sends one command and checks the reply code. $secret keeps it out of error logs. */
function smtp_cmd($sock, string $line, $expect, bool $secret = false): string
{
    if (fwrite($sock, $line . "\r\n") === false) {
        throw new RuntimeException('SMTP write failed');
    }
    try {
        return smtp_expect($sock, $expect);
    } catch (RuntimeException $e) {
        $shown = $secret ? '[hidden]' : strtok($line, "\r\n");
        throw new RuntimeException("After '{$shown}': " . $e->getMessage());
    }
}

/** Reads a (possibly multi-line) reply and checks its status code. */
function smtp_expect($sock, $expect): string
{
    $reply = '';
    while (($line = fgets($sock, 1024)) !== false) {
        $reply .= $line;
        if (strlen($line) < 4 || $line[3] === ' ') {
            break;
        }
    }
    $code = (int)substr($reply, 0, 3);
    if (!in_array($code, (array)$expect, true)) {
        throw new RuntimeException('SMTP replied: ' . trim($reply ?: '(no response)'));
    }
    return $reply;
}

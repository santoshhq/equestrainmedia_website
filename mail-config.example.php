<?php
/*
 * SMTP settings for send-mail.php.
 *
 * Copy this file to mail-config.php and fill in the mailbox details from
 * cPanel → Email Accounts → (your account) → Connect Devices.
 * mail-config.php holds a password: never commit it or share it.
 */
return [
    // Outgoing server, e.g. mail.equestrianmedia.in
    'host'       => 'mail.equestrianmedia.in',
    // 465 with 'ssl', or 587 with 'tls'
    'port'       => 465,
    'encryption' => 'ssl',

    // Full mailbox address and its password
    'username'   => 'sales@equestrianmedia.in',
    'password'   => 'CHANGE_ME',

    // Sender shown on the notification; keep it the same as username
    'from_email' => 'sales@equestrianmedia.in',
    'from_name'  => 'Equestrian Media Website',

    // Where new enquiries are delivered
    'to_email'   => 'sales@equestrianmedia.in',
];

<?php

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    // Extract data from the form
    $name = $_POST["name"];
    $email = $_POST["email"];
    $message = $_POST["message"];

    // Validate and process the data (customize this part based on your needs)
    if (empty($name) || empty($email) || empty($message)) {
        // Handle validation errors, e.g., redirect back to the form with an error message
        header("Location: contact-us.php?error=empty_fields");
        exit();
    }

    // Process the contact form data (customize this part based on your needs)
    // You might want to send an email, store the data in a database, or perform other actions

    // For example, log the data to a file
    $file = 'contact_submissions.txt';
    $data = json_encode([
        'name' => $name,
        'email' => $email,
        'message' => $message,
    ]) . PHP_EOL;
    file_put_contents($file, $data, FILE_APPEND);

    // Redirect back to a thank-you page or the homepage
    header("Location: thank-you-contact.php");
    exit();
} else {
    // If someone tries to access this script directly, redirect them to the homepage
    header("Location: index.php");
    exit();
}

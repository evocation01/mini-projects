<?php
// Path to the scores file
$scoresFile = 'scores.txt';

// Get the input data from the POST request
$data = file_get_contents('php://input');

// Validate input
if (!$data) {
    http_response_code(400); // Bad Request
    echo "Invalid input.";
    exit;
}

// Append the new score to the file
file_put_contents($scoresFile, $data . PHP_EOL, FILE_APPEND);

// Return success response
echo "Score updated successfully.";
?>

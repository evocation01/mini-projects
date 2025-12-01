<?php
// Path to the scores file
$scoresFile = 'scores.txt';

// Check if the file exists
if (file_exists($scoresFile)) {
    // Read and output the file contents
    echo file_get_contents($scoresFile);
} else {
    // If the file doesn't exist, return an empty response
    echo '';
}
?>

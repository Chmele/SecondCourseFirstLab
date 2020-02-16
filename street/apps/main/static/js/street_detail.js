var right = document.getElementById("right_sidebar");
function open_right(){
  if (right.style.display === 'block') {
    right.style.display = 'none';
    overlayBg.style.display = "none";
  } else {
    right.style.display = 'block';
    overlayBg.style.display = "block";
  }
}

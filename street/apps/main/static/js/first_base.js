var mySidebar = document.getElementById("mySidebar");
    function w3_open() {
        console.log(mySidebar.style.display);
      if (mySidebar.style.display === 'block') {
        mySidebar.style.display = 'none';
        
      } else {
        mySidebar.style.display = 'block';
      }
    }
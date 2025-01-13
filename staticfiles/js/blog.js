const buttonOne = document.getElementById('btnOne');
const buttonTwo = document.getElementById('btnTwo');
const buttonThree = document.getElementById('btnThree');
const contentArea = document.getElementById('main-content')
const page1Cont = document.getElementById('content')
const page2Cont = document.getElementById('create')
const page3Cont = document.getElementById('community')


function displayPageOne() {
    page1Cont.style.display = "block"
    page2Cont.style.display = "none"
    page3Cont.style.display = "none"
    
   // buttonOne.classList.add('nav-link-selected')
  //  buttonTwo.classList.remove('nav-link-selected')
  //  buttonThree.classList.remove('nav-link-selected')
}

buttonOne.addEventListener('click', displayPageOne)


function displayPageTwo() {
    page1Cont.style.display = "none"
    page2Cont.style.display = "block"
    page3Cont.style.display = "none"
  //  buttonOne.classList.remove('nav-link-selected')
  //  buttonTwo.classList.add('nav-link-selected')
  //  buttonThree.classList.remove('nav-link-selected')
}

buttonTwo.addEventListener('click', displayPageTwo)


function displayPageThree() {
    page1Cont.style.display = "none"
    page2Cont.style.display = "none"
    page3Cont.style.display = "block"
  //  buttonOne.classList.remove('nav-link-selected')
   // buttonTwo.classList.remove('nav-link-selected')
   // buttonThree.classList.add('nav-link-selected')
}

buttonThree.addEventListener('click', displayPageThree)


// For image upload 
document.getElementById('fileInput').addEventListener('change', function() {
  var fileName = this.files[0] ? this.files[0].name : 'No file chosen';
  document.getElementById('fileName').textContent = fileName;
}); 

const dropArea = document.getElementById("drop-area");
const fileInput = document.getElementById("fileElem");
const fileName = document.querySelector(".file-name");

if (dropArea) {

    ["dragenter","dragover"].forEach(eventName => {

        dropArea.addEventListener(eventName, e => {

            e.preventDefault();

            dropArea.classList.add("highlight");

        });

    });

    ["dragleave","drop"].forEach(eventName => {

        dropArea.addEventListener(eventName, e => {

            e.preventDefault();

            dropArea.classList.remove("highlight");

        });

    });

    dropArea.addEventListener("drop", e => {

        const files = e.dataTransfer.files;

        fileInput.files = files;

        fileName.innerHTML = "📄 " + files[0].name;

    });

    fileInput.addEventListener("change", () => {

        if(fileInput.files.length>0){

            fileName.innerHTML="📄 "+fileInput.files[0].name;

        }

    });

}
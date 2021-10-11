// Version 0.0.1, Specific to app page
const from=document.querySelector("#from"),file=document.querySelector("#file"),_to=document.querySelector("#to");from.addEventListener("change",function(e){const{value:t}=this;file.setAttribute("accept",`.${t}`),file.removeAttribute("disabled")});

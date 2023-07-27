
function sendValue(value) {
  Streamlit.setComponentValue(value)
}


function onRender(event) {
  if (!window.rendered) {
    const {label, value } = event.detail.args;
    const input = document.getElementById("search");
    const btn = document.getElementById("go");

    if (label) {
      input.setAttribute("placeholder",label)
    }

    if (value && !input.value) {
      input.value = value
    }

    input.onkeydown=function(event){
      if(event.key === 'Enter') {
        sendValue(input.value);
    }
    }
    btn.onclick = function (){
      sendValue(input.value);
    }

    window.rendered = true
  }
}


Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)

Streamlit.setComponentReady()

Streamlit.setFrameHeight(65)

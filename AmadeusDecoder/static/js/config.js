
function tabClicked(tabId) {
    const activeTab = document.querySelector('.nav-item .active');
    const activePanel = document.querySelector('.tab-content.general .tab-pane.active');
    
    if (activeTab) {
        console.log("Salut");
        console.log('active ta:', activeTab.id);
        activeTab.classList.remove('active');
    }

    if (activePanel) {
        activePanel.classList.remove('active','show');
        console.log('active pa:',activePanel.id);
    }

    // Activez l'onglet et le panneau correspondants
    const newTab = document.getElementById(tabId);
    const newPanel = document.getElementById(`${tabId}-panel`);
    console.log('newPanel :',newPanel.id);
    console.log(newPanel);
    if (newTab && newPanel) {
        newTab.classList.add('active');
        newPanel.classList.add('active','show');
    }
}

$(document).ready(function() {
    // Gérer le clic sur une ligne
    $('#trEmailPnrModal').click(function() {

      $('#modalEmailPnrEnv').val($(this).data('env'));
      $('#modalEmailPnrEmail').val($(this).data('email'));
      $('#modalEmailPnrPassword').val($(this).data('password'));

    });

    $('#trEmailNotifModal').click(function() {
        console.log('trEmailNotifModal');
      $('#modalNotifEnv').val($(this).data('env'));
      $('#modalNotifValueName').val($(this).data('value-name'));
      $('#modalNotifEmail').val($(this).data('email'));

    });

    $('#trEmailNotifSenderModal').click(function() {
        console.log('trEmailNotifSenderModal');
      $('#modalNotifSenderEnv').val($(this).data('env'));
      $('#modalNotifSenderValueName').val($(this).data('value-name'));
      $('#modalNotifSenderEmail').val($(this).data('email'));
      $('#modalNotifSenderPassword').val($(this).data('password'));
      $('#modalSmtp').val($(this).data('smtp'));
      $('#modalPort').val($(this).data('port'));

    });

     $('#trEmailFeesModal').click(function() {
        console.log('trEmailFeesModal');
      $('#modalFeesEnv').val($(this).data('env'));
      $('#modalFeesValueName').val($(this).data('value-name'));
      $('#modalFeesEmail').val($(this).data('email'));

    });

    $('#trEmailFeesRequestModal').click(function() {
        console.log('trEmailFeesRequestModal');
      $('#modalFeesRequestEnv').val($(this).data('env'));
      $('#modalFeesRequestSenderEmail').val($(this).data('sender-email'));
      $('#modalFeesRequestRecipientEmail').val($(this).data('recipient-email'));

    });
  });

const ul = document.querySelector("#insertmodalul"),
input = ul.querySelector("input");
let tags =[];

$(document).ready(function() {
    $('.trModalInsert').click(function() {
        var modal = $('#' + this.id);
        console.log("modal",modal);
        $('#modalLabel').text(modal.data('value-name'));
        console.log(this.id);
        var value = modal.data('value');
        var liste = value.split(',');
        var ul = document.querySelector("#insertmodalul");
        ul.querySelectorAll("li").forEach(li =>li.remove());
        console.log(liste);
        liste.forEach(element => {
            let li = `<li>${element} <i class="fa fa-xmark" onclick="remove(this, '${element}')" ></i></li>`;
            ul.insertAdjacentHTML("afterbegin", li);
            tags.push(element);
        });
        console.log('tags:', tags);

    });

    $('#closeinsertmodal').click(function () {
        console.log('modal closed');
        removeAll();
        ul.querySelectorAll("li").forEach(li => console.log(li.textContent));
    });

});

function removeAll() {
    ul.querySelectorAll("li").forEach(li =>li.remove());
}


function CreateTag(){
    ul.querySelectorAll("li").forEach(li =>li.remove());
    tags.slice().reverse().forEach(tag => {
        let liTag = `<li>${tag} <i class="fa fa-xmark" onclick="remove(this, '${tag}')" ></i></li>`;
        ul.insertAdjacentHTML("afterbegin", liTag);
    });
}

function remove(element, tag){
    let index = tags.indexOf(tag);
    tags = [...tags.slice(0,index), ...tags.slice(index+1)];
    element.parentElement.remove();
}

function addTag(e){
    if(e.key == "Enter"){

        let tag = e.target.value;
        if (tag.length >1 && !tags.includes(tag)) {
            tag.split(',').forEach(tag => {
                tags.push(tag);
                CreateTag();
                console.log(tags);
            });
        }
        e.target.value ="";
    }
}

input.addEventListener("keyup", addTag);


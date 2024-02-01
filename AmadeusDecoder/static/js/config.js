
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
let multiInputTags =[];
let finalMultiInsertTags = [];

const multiInsertwrapper = document.querySelectorAll(".multiInsertwrapper");

$(document).ready(function() {
    $('.trModalInsert').click(function() {
        var tr = document.getElementById(this.id);

        $('#modalLabel').text(tr.dataset.valuename);
        var value = tr.dataset.value;
        var liste = value.split(',');
        var ul = document.querySelector("#insertmodalul");

        ul.querySelectorAll("li").forEach(li =>li.remove());
        tags=[];
        console.log('liste',liste);

        liste.forEach(element => {
            console.log('element',element);
            let li = `<li>${element} <i class="fa fa-xmark" onclick="remove(this, '${element}')" ></i></li>`;
            ul.insertAdjacentHTML("afterbegin", li);
            tags.push(element);
        });
        console.log('tags:', tags);

    });

    $('#closeinsertmodal').click(function () {
        console.log('modal closed');
        removeAllModal();
    });

});


function removeAllModal() {
    ul.querySelectorAll("li").forEach(li =>li.remove());
}

function CreateTag(){
    // localStorage.setItem("tablist", JSON)
    ul.querySelectorAll("li").forEach(li =>li.remove());
    tags.slice().reverse().forEach(tag => {
        let liTag = `<li>${tag} <i class="fa fa-xmark" onclick="remove(this, '${tag}')" ></i></li>`;
        ul.insertAdjacentHTML("afterbegin", liTag);
    });
}

function remove(element, tag){
    let index = tags.indexOf(tag);
    // console.log(Array.isArray(tags_utilise));
    // tags_utilise = Array.from(tags_utilise);
    tags = tags.filter(element => element !== tag);
    // tags.splice(index, 1);
    console.log('tag after remove :',tags );
    element.parentElement.remove();
}

function addTag(e){
    if(e.key == "Enter"){

        let tag = e.target.value;
        if (tag.length >1 && !tags.includes(tag)) {
            tag.split(',').forEach(tag => {
                tags.push(tag);
                CreateTag(tags, ul);
                console.log('addTag : ',tags);
                finalMultiInsertTags.push(tags);
            });
        }
        e.target.value ="";
    }
}

input.addEventListener("keyup", addTag);


// multiInsertwrapper.forEach(wrapper => {
//     const ul = wrapper.querySelector('.multiInsertcontent ul');
//     const input = wrapper.querySelector('.multiInsertcontent input');
//     let multiInputtags =[];

//     input.addEventListener("keyup",(e) => {
//         addTag(e,multiInputtags,ul);
//     });

//     const Button = wrapper.querySelector('.multiInsertdetail button');
//     $(Button).click(function () {
//         console.log('click');
//         ul.querySelectorAll("li").forEach(li =>li.remove());
//         multiInputtags = [];
//         finalMultiInsertTags.push(multiInputtags);
//     });
//     console.log('final :',finalMultiInsertTags);
// });

$(document).ready(function () {
    $('#saveIt').click(function () {
        console.log('save it :',finalMultiInsertTags);
    })    
});

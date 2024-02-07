$(document).ready(function() {
    $('#name').hide();
    $('#currency_name').hide();
    $('#currency_code').hide();
    $('#language_code').hide();
    $('#regional_country').hide();
    $('#generalInfoFooter').hide();
    $('.insertmodalwrapper.regional_country').hide();
});

const ul = document.querySelector(".insertmodalul"),
input = ul.querySelector("input");
let tags =[];
let multiInputTags =[];
let finalMultiInsertTags = [];

const multiInsertwrapper = document.querySelectorAll(".multiInsertwrapper");


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

// All modal data 
$(document).ready(function() {
    $('#trSavingFileModal').click(function() {
        
      $('#modalLinkEnv').val($(this).data('env'));
      $('#modalLink').val($(this).data('link'));

    });

    $('#trEmailPnrModal').click(function() {

      $('#modalEmailPnrEnv').val($(this).data('env'));
      $('#modalEmailPnrEmail').val($(this).data('email'));
      $('#modalEmailPnrPassword').val($(this).data('password'));

    });

    $('.trEmailNotifModal').click(function() {
        
      $('#modalNotifEnv').val($(this).data('env'));
      $('#modalNotifValueName').val($(this).data('value-name'));
      $('#modalNotifValueName').text($(this).data('value'));

      $('#modalNotifEmail').val($(this).data('email'));

      const ul_list = $(this).find('.ul_list li');
        var liste = [];
        ul_list.each(function() {
            liste.push($(this).text());
        });

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

    $('.trEmailNotifSenderModal').click(function() {
      $('#modalNotifSenderEnv').val($(this).data('env'));
      $('#modalNotifSenderValueName').val($(this).data('value-name'));
      $('#modalNotifSenderValueName').text($(this).data('value'));
      $('#modalNotifSenderEmail').val($(this).data('email'));
      $('#modalNotifSenderPassword').val($(this).data('password'));
      $('#modalSmtp').val($(this).data('smtp'));
      $('#modalPort').val($(this).data('port'));

    });

     $('.trEmailFeesModal').click(function() {
        const ul_list = $(this).find('.ul_list li');
        var liste = [];
        ul_list.each(function() {
            liste.push($(this).text());
        });

        ul.querySelectorAll("li").forEach(li =>li.remove());
        tags=[];

        liste.forEach(element => {
            console.log('element',element);
            let li = `<li>${element} <i class="fa fa-xmark" onclick="remove(this, '${element}')" ></i></li>`;
            ul.insertAdjacentHTML("afterbegin", li);
            tags.push(element);
        });
      $('#modalFeesEnv').val($(this).data('env'));
      $('#modalFeesValueName').val($(this).data('value-name'));
      $('#modalFeesValueName').text($(this).data('value'));
      $('#modalFeesEmail').val($(this).data('email'));

    });

    $('.trEmailFeeSenderModal').click(function() {
      $('#modalFeeSenderEnv').val($(this).data('env'));
      $('#modalFeeSenderValueName').val($(this).data('value-name')).text($(this).data('value'));
      $('#modalFeeSenderEmail').val($(this).data('email'));
      $('#modalFeeSenderPassword').val($(this).data('password'));
      $('#modalFeeSenderSmtp').val($(this).data('smtp'));
      $('#modalFeeSenderPort').val($(this).data('port'));
    });
  });



// Update data
$(document).ready(function() {
    $('.trModalInsert').click(function() {
        var tr = document.getElementById(this.id);

        $('#modalLabel').text(tr.dataset.valuename);
        var value = tr.dataset.value;
        console.log(value);
        value = value.replace(/'/g, '"');
        
        var liste = JSON.parse(value)
        var ul = document.querySelector(".insertmodalul");

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
    ul.querySelectorAll("li").forEach(li =>li.remove());
    tags.slice().reverse().forEach(tag => {
        let liTag = `<li>${tag} <i class="fa fa-xmark" onclick="remove(this, '${tag}')" ></i></li>`;
        ul.insertAdjacentHTML("afterbegin", liTag);
    });
}

function remove(element, tag){
    tags = tags.filter(element => element !== tag);
    element.parentElement.remove();
}

function addTag(e){
    console.log("Input !!!");
    if(e.key == "Enter"){
        console.log("Enter !!!!!!");
        let tag = e.target.value;
        if (tag.length >1 && !tags.includes(tag)) {
            tag.split(',').forEach(tag => {
                tags.push(tag);
                CreateTag();
            });
        }
        e.target.value ="";
    }
}

input.addEventListener("keyup", addTag);

// Multi-input
multiInsertwrapper.forEach(wrapper => {
    const multiInputUl = wrapper.querySelector('.multiInsertcontent ul');
    const multiInputInput = wrapper.querySelector('.multiInsertcontent input');
    let multiInputtags =[];

    multiInputInput.addEventListener("keyup",(e) => {
        if(e.key == "Enter"){
        let tag = e.target.value;
        if (tag.length >1 && !multiInputtags.includes(tag)) {
            tag.split(',').forEach(tag => {
                multiInputtags.push(tag);
                multiInputUl.querySelectorAll("li").forEach(li =>li.remove());
                multiInputtags.slice().reverse().forEach(tag => {
                    let liTag = `<li>${tag} <i class="fa fa-xmark removeIcon"  ></i></li>`;
                    multiInputUl.insertAdjacentHTML("afterbegin", liTag);
                });
                finalMultiInsertTags=[];
                finalMultiInsertTags.push(multiInputtags);
            });
        }
        e.target.value ="";
    }
    });

    multiInputUl.addEventListener("click", function (e) {
        if (e.target.classList.contains("removeIcon")) {
            const li = e.target.closest("li");
            const li_tag = li.innerText;

            multiInputtags = multiInputtags.filter(element => element !== li_tag);
            multiInputUl.querySelectorAll("li").forEach(li =>li.remove());
            multiInputtags.slice().reverse().forEach(tag => {
                let liTag = `<li>${tag} <i class="fa fa-xmark removeIcon"  ></i></li>`;
                multiInputUl.insertAdjacentHTML("afterbegin", liTag);
            });
            finalMultiInsertTags = [];
            finalMultiInsertTags.push(multiInputtags); 
        }
    });

    const Button = wrapper.querySelector('.multiInsertdetail button');
    $(Button).click(function () {
        console.log('click');
        multiInputUl.querySelectorAll("li").forEach(li =>li.remove());
        finalMultiInsertTags = finalMultiInsertTags.filter(element => element !== multiInputtags );
        console.log('final :',finalMultiInsertTags);
    })

});

$(document).ready(function () {
    $('#saveIt').click(function () {
        multiInsertwrapper.forEach(wrapper => {
        const multiInputUl = wrapper.querySelector('.multiInsertcontent ul');
        const multiInputInput = wrapper.querySelector('.multiInsertcontent input');
            console.log(multiInputInput.getAttribute('name'));
            multiInputUl.querySelectorAll("li").forEach(li =>console.log(li.textContent));
        })
    });  
})

// ---------------- All Update functions ------------------------

// Update Company Information
function updateGeneralInfo(){
    $('#name_label').hide();
    $('#currency_name_label').hide();
    $('#currency_code_label').hide();
    $('#language_code_label').hide();
    $('.list-group.ol_list').hide();

    $('.insertmodalwrapper.regional_country').show();

    // multi insert regional country 
    const ol_list = document.querySelectorAll('.list-group.ol_list li');
    var liste = [];
    ol_list.forEach(li => {
        liste.push(li.innerText);
    });

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

    $('#name').show();
    $('#currency_name').show();
    $('#currency_code').show();
    $('#language_code').show();
    $('#regional_country').show();
    $('#generalInfoFooter').show();
    
}

// Update Email pnr
function UpdateEmailPnr() {
    var env = $('#modalEmailPnrEnv').val();
    var email = $('#modalEmailPnrEmail').val();
    var password = $('#modalEmailPnrPassword').val();
    console.log(email);
    console.log(password);

    $.ajax({
        type: "POST",
        url: "/setting/email-pnr-update",
        dataType: "json",
        data: {
            email: email,
            password: password,
            csrfmiddlewaretoken: csrftoken,
        },
        success: function (data) {
            if (data == 'ok') {
                toastr.success('Information(s) modifiée(s)');
                setTimeout(() => {
                    location.reload();
                }, 1000)
            } 
            if (data.status == 'error') {
                toastr.error(data.error)
            }
        },
    });
}


$(document).ready(function () {
    // Update Company Informations
    $('#updateGeneralInfo').click(function () {
        var name = $("#name").val();
        var currency_name = $('#currency_name').val();
        var currency_code = $('#currency_code').val();
        var language_code = $('#language_code').val();

        $.ajax({
            type: "POST",
            url: "/setting/general-update",
            dataType: "json",
            data: {
                name: name,
                currency_name: currency_name,
                currency_code: currency_code,
                language_code: language_code,
                regional_country: JSON.stringify(tags),
                csrfmiddlewaretoken: csrftoken,
            },
            success: function (data) {
                if (data == 'ok') {
                    toastr.success('Information(s) modifiée(s)');
                    setTimeout(() => {
                        location.reload();
                    }, 1000)
                } 
                if (data.status == 'error') {
                    toastr.error(data.error)
                }
            },
        });
    })

    // Update Saving File Protocol
    $('#buttonUpdateSavingFile').click(function () {
        var link = $('#modalLink').val();
        var env = $('#modalLinkEnv').val();

        $.ajax({
            type: "POST",
            url: "/setting/saving-protocol-update",
            dataType: "json",
            data: {
                link: link,
                env: env,
                csrfmiddlewaretoken: csrftoken,
            },
            success: function (data) {
                if (data == 'ok') {
                    toastr.success('Information(s) modifiée(s)');
                    setTimeout(() => {
                        location.reload();
                    }, 1000)
                } 
                if (data.status == 'error') {
                    toastr.error(data.error)
                }
            },
        });
    })


})

// Update Email Notifications
function UpdateEmailNotifSender(){
    var port = $('#modalPort').val();
    var smtp = $('#modalSmtp').val();
    var email = $('#modalNotifSenderEmail').val();
    var password = $('#modalNotifSenderPassword').val();
    var ValueName = $('#modalNotifSenderValueName').val();

    $.ajax({
        type: "POST",
        url: "/setting/email-notif-sender-update",
        dataType: "json",
        data: {
            port:port,
            smtp:smtp,
            email: email,
            password: password,
            valuename: ValueName,
            csrfmiddlewaretoken: csrftoken,
        },
        success: function (data) {
            if (data == 'ok') {
                toastr.success('Information(s) modifiée(s)');
                setTimeout(() => {
                    location.reload();
                }, 1000)
            } 
            if (data.status == 'error') {
                toastr.error(data.error)
            }
        },
    });
}

function UpdateEmailNotif(){
    console.log('tagssss : ',tags);
    var email = JSON.stringify(tags);
    var ValueName = $('#modalNotifValueName').val();
    
    $.ajax({
        type: "POST",
        url: "/setting/email-notif-update",
        dataType: "json",
        data: {
            email: email,
            valuename: ValueName,
            csrfmiddlewaretoken: csrftoken,
        },
        success: function (data) {
            if (data == 'ok') {
                toastr.success('Information(s) modifiée(s)');
                setTimeout(() => {
                    location.reload();
                }, 1000)
            } 
            if (data.status == 'error') {
                toastr.error(data.error)
            }
        },
    });
}

function UpdateEmailFees() {
    console.log('tagssss : ',tags);
    var email = JSON.stringify(tags);
    var ValueName = $('#modalFeesValueName').val();
    
    $.ajax({
        type: "POST",
        url: "/setting/email-fees-update",
        dataType: "json",
        data: {
            email: email,
            valuename: ValueName,
            csrfmiddlewaretoken: csrftoken,
        },
        success: function (data) {
            if (data == 'ok') {
                toastr.success('Information(s) modifiée(s)');
                setTimeout(() => {
                    location.reload();
                }, 1000)
            } 
            if (data.status == 'error') {
                toastr.error(data.error)
            }
        },
    });
}

function UpdateEmailFeeSender(){
    var port = $('#modalFeeSenderPort').val();
    var smtp = $('#modalFeeSenderSmtp').val();
    var email = $('#modalFeeSenderEmail').val();
    var password = $('#modalFeeSenderPassword').val();
    var ValueName = $('#modalFeeSenderValueName').val();

    $.ajax({
        type: "POST",
        url: "/setting/email-fee-sender-update",
        dataType: "json",
        data: {
            port:port,
            smtp:smtp,
            email: email,
            password: password,
            valuename: ValueName,
            csrfmiddlewaretoken: csrftoken,
        },
        success: function (data) {
            if (data == 'ok') {
                toastr.success('Information(s) modifiée(s)');
                setTimeout(() => {
                    location.reload();
                }, 1000)
            } 
            if (data.status == 'error') {
                toastr.error(data.error)
            }
        },
    });
}

// Update multiInsert
function UpdateMultiInput(){
    var value_name = $('#modalLabel').text();
    console.log("update multi input");
    console.log(value_name);
    console.log(tags);
    
    $.ajax({
        type: "POST",
        url: "/setting/parsing-update",
        dataType: "json",
        data: {
            tags: JSON.stringify(tags),
            valuename: value_name,
            csrfmiddlewaretoken: csrftoken,
        },
        success: function (data) {
            if (data == 'ok') {
                toastr.success('Information(s) modifiée(s)');
                setTimeout(() => {
                    location.reload();
                }, 1000)
            } 
            if (data.status == 'error') {
                toastr.error(data.error)
            }
        },
    });
}

function redirectToTab(tabId){
    $('#'+tabId).tab('show');
}

// ------------------ All Create Functions--------------------

function CreateCompany(){
    var name = $('#create_name').val();
    var currency_name = $('#create_currency_name').val();
    var currency_code = $('#create_currency_code').val();
    var language_code = $('#create_language_code').val();
    console.log('finalMultiInsertTags', finalMultiInsertTags);
    
    $.ajax({
            type: "POST",
            url: "/setting/general-information-create",
            dataType: "json",
            data: {
                name: name,
                currency_name: currency_name,
                currency_code: currency_code,
                language_code: language_code,
                regional_country: JSON.stringify(finalMultiInsertTags[0]),
                csrfmiddlewaretoken: csrftoken,
            },
            success: function (data) {
                if (data == 'ok') {
                    toastr.success('Informations Enregistrées');
                    setTimeout(() => {
                        location.reload();
                    }, 1000)
                } 
                if (data.status == 'error') {
                    toastr.error(data.error)
                }
            },
        });

}
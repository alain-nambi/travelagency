$(document).ready(function() {

    $('.insertmodalwrapper.regional_country').hide();
     $('.card.EmailNotifCard').hide();
});

const ul = document.querySelector(".insertmodalul"),
input = ul.querySelector("input");
let tags =[];
let multiInputTags =[];
let finalMultiInsertTags = [];

const multiInsertwrapper = document.querySelectorAll(".multiInsertwrapper");

const ulNotification = document.querySelector(".insertmodalul.notification")
const ulFees = document.querySelector(".insertmodalul.fee")


function tabClicked(tabId) {
    const activeTab = document.querySelector('.nav-item .active');
    const activePanel = document.querySelector('.tab-content.general .tab-pane.active');
    
    if (activeTab) {
        
        activeTab.classList.remove('active');
    }

    if (activePanel) {
        activePanel.classList.remove('active','show');
    }

    // Activez l'onglet et le panneau correspondants
    const newTab = document.getElementById(tabId);
    const newPanel = document.getElementById(`${tabId}-panel`);
    
    
    if (newTab && newPanel) {
        newTab.classList.add('active');
        newPanel.classList.add('active','show');
    }
}

// All modal data 
$(document).ready(function() {
    $('#trSavingFileModal').click(function() {
        
      $('#modalLinkEnv').val($(this).data('env'));
      $('#modal_storage').val($(this).data('storage'));
      $('#modal_hostname').val($(this).data('hostname'));
      $('#modal_username').val($(this).data('username'));
      $('#modal_password').val($(this).data('password'));
      $('#modal_repository').val($(this).data('repository'));
      $('#modal_port').val($(this).data('port'));
      $('#modal_link').val($(this).data('link'));
      

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

        ulNotification.querySelectorAll("li").forEach(li =>li.remove());
        tags=[];
        

        liste.forEach(element => {
            
            let li = `<li>${element} <i class="fa fa-xmark" onclick="remove(this)" ></i></li>`;
            ulNotification.insertAdjacentHTML("afterbegin", li);
            tags.push(element);
        });
        

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
        

        $('#modalFeesEnv').val($(this).data('env'));
        $('#modalFeesValueName').val($(this).data('value-name'));
        $('#modalFeesValueName').text($(this).data('value'));
        $('#modalFeesEmail').val($(this).data('email'));
        const ul_list = $(this).find('.ul_list li');
        var liste = [];
        ul_list.each(function() {
            liste.push($(this).text());
        });

        
        ulFees.querySelectorAll("li").forEach(li =>li.remove());
        tags=[];
        liste.forEach(element => {
            let li = `<li>${element}<i class="fa fa-xmark" onclick="remove(this)"></i></li>`;
            ulFees.insertAdjacentHTML("afterbegin", li);
            tags.push(element);
        });
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



// Update data // value = value.replace(/'/g, '"');
$(document).ready(function() {
    $('.trModalInsert').click(function() {
        var tr = document.getElementById(this.id);

        $('#modalLabel').text(tr.dataset.valuename);
        var value = tr.dataset.value;
        // Supprimer les espaces après une virgule
        value = value.replace(/,\s+/g, ',');

        // transform array of array to array ( [['a','b']] => ["a,b"] )
        if (tr.dataset.valuename == "Itinerary header possible format") {
            value = value.replace(/'/g, '')
            value = value.replace(/,\[/g, ',"');
            value = value.replace(/\],/g, '",');
            value = value.replace(/\]]/g, '"]');
            value = value.replace(/\[\[/g, '["');
        }
        
        // transform dict to aray ( {'key':'value'} => ["key:value"])
        if (tr.dataset.valuename == "Contact type names"){
            // transform {} => []
            value = value.replace(/{/g, '[').replace(/}/g, ']');

            //Supprimer les espaces après :
            value = value.replace(/:\s+/g, ':');

            // enlever les quotes avant et après une virgule
            value = value.replace(/':'/g,':');

            // Remplacer les apostrophes par des guillemets doubles
            value = value.replace(/'/g, '"');

        }

        else {
            // Remplacer les apostrophes avant et après une virgule par des guillemets doubles
            value = value.replace(/,'/g, ',"').replace(/',/g, '",');
            // Remplacer le premier et le dernier apostrophe par des guillemets doubles
            value = value.replace(/\['/g, '["').replace(/'\]/g, '"]');
        }
        
        console.log("value : ", value);

        var liste = JSON.parse(value)
        var ul = document.querySelector(".insertmodalul");

        ul.querySelectorAll("li").forEach(li =>li.remove());
        tags=[];

        liste.forEach(element => {
            let li = `<li>${element} <i class="fa fa-xmark" onclick="remove(this)" ></i></li>`;
            ul.insertAdjacentHTML("afterbegin", li);
            tags.push(element);
        });
        console.log(liste);
        console.log(tags);
        
    });


    $('#closeinsertmodal').click(function () {
        removeAllModal();
    });

});

function removeAllModal() {
    ul.querySelectorAll("li").forEach(li =>li.remove());
    tags = [];
}

function CreateTag(target){
    target.parentElement.querySelectorAll("li").forEach(li =>li.remove());
    tags.slice().reverse().forEach(tag => {
        let liTag = `<li>${tag} <i class="fa fa-xmark" onclick="remove(this)" ></i></li>`;
        
        target.parentElement.insertAdjacentHTML("afterbegin", liTag);
    });
}

function remove(element){
    var tag = element.parentNode.firstChild.nodeValue.trim();

    tags = tags.filter(element => element !== tag);
    console.log("remove : ",tags);
    element.parentElement.remove();
}

function addTag(e){
    
    if(e.key == "Enter"){
        const target = e.target
        let tag = e.target.value;
        if (tag.length > 1 && !tags.includes(tag)) {
            tags.push(tag);
            CreateTag(target);
        }
        e.target.value ="";
    }
}

if (ulFees && ulFees.querySelector('input')) {
    ulFees.querySelector('input').addEventListener("keyup", addTag)
}

if (ulNotification && ulNotification.querySelector('input')) {
    ulNotification.querySelector('input').addEventListener("keyup", addTag)
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
            
            multiInputtags.push(tag);
            multiInputUl.querySelectorAll("li").forEach(li =>li.remove());
            multiInputtags.slice().reverse().forEach(tag => {
                let liTag = `<li>${tag} <i class="fa fa-xmark removeIcon"  ></i></li>`;
                multiInputUl.insertAdjacentHTML("afterbegin", liTag);
            });
            finalMultiInsertTags=[];
            finalMultiInsertTags.push(multiInputtags);
            
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
        
        multiInputUl.querySelectorAll("li").forEach(li =>li.remove());
        multiInputtags = [];
        console.log(multiInputtags);
        finalMultiInsertTags = [];
        
    })

});


// ---------------- All Update functions ------------------------

// Update Company Information
function updateGeneralInfo(){
    $('#name_label').hide();
    $('#currency_name_label').hide();
    $('#currency_code_label').hide();
    $('#language_code_label').hide();
    $('.ul_list').hide();

    document.getElementById('regional_country').hidden = false;
    document.getElementById('regional_country').style.display = 'block';

    document.getElementById('modif_footer').hidden = false;


    // multi insert regional country 
    const ol_list = document.querySelectorAll('.ul_list li');
    var liste = [];
    ol_list.forEach(li => {
        liste.push(li.innerText);
    });

    ul.querySelectorAll("li").forEach(li =>li.remove());
    tags=[];
    

    liste.forEach(element => {
        
        let li = `<li>${element} <i class="fa fa-xmark" onclick="remove(this)" ></i></li>`;
        ul.insertAdjacentHTML("afterbegin", li);
        tags.push(element);
    });
    
    document.getElementById('name').hidden = false;
    document.getElementById('currency_name').hidden = false;
    document.getElementById('currency_code').hidden = false;
    document.getElementById('language_code').hidden = false;
    
}

// Update Email pnr
function UpdateEmailPnr() {
    var env = $('#modalEmailPnrEnv').val();
    var email = $('#modalEmailPnrEmail').val();
    var password = $('#modalEmailPnrPassword').val();    

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
                    location.reload();
            } 
            if (data.status == 'error') {
                toastr.error(data.error)
            }
        },
    });
}


$(document).ready(function () {
    // Update Company Informations
    $('#GeneralInfoUpdate').click(function () {
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
                            location.reload();

                } 
                if (data.status == 'error') {
                    toastr.error(data.error)
                }
            },
        });
    })

    // Update Saving File Protocol
    $('#buttonUpdateSavingFile').click(function () {
        var link = $('#modal_link').val();
        var storage = $('#modal_storage').val();
        var hostname = $('#modal_hostname').val();
        var username = $('#modal_username').val();
        var password = $('#modal_password').val();
        var repository = $('#modal_repository').val();
        var port = $('#modal_port').val();

        var env = $('#modalLinkEnv').val();
        
        
        $.ajax({
            type: "POST",
            url: "/setting/saving-protocol-update",
            dataType: "json",
            data: {
                link: link,
                storage: storage,
                hostname: hostname,
                username: username,
                password: password,
                repository: repository,
                port: port,
                env: env,
                csrfmiddlewaretoken: csrftoken,
            },
            success: function (data) {
                if (data == 'ok') {
                    toastr.success('Information(s) modifiée(s)');
                            location.reload();

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
                    location.reload();
            } 
            if (data.status == 'error') {
                toastr.error(data.error)
            }
        },
    });
}

function UpdateEmailNotif(){
    
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
                    location.reload();
            } 
            if (data.status == 'error') {
                toastr.error(data.error)
            }
        },
    });
}

function UpdateEmailFees() {
    
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
                    location.reload();
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
                    location.reload();
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
    let state = 'ok';
    if (value_name == "Itinerary header possible format"){
        tags.forEach(element => {
            element = element.split(',');
            if(element.length != 9){
                toastr.error('Veuillez entrer neuf élément pour ce champ');
                state = 'not ok'
            }
            else{
                state = 'ok'
            }
        });
    }
    if (state == 'ok'){
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
                        location.reload();
                } 
                if (data.status == 'error') {
                    toastr.error(data.error)
                }
            },
        });
    }
    
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
                            location.reload();

                } 
                if (data.status == 'error') {
                    toastr.error(data.error)
                }
            },
        });

}

$('#create_storage').on('change', function () {
    if ($(this).val() == 'Local') {
        $('#create_hostname').hide();
        $('#create_port').hide();
        $('#create_username').hide();
        $('#create_password').hide();
        $('#create_repository').hide();
        $('#hostname_label').hide();
        $('#port_label').hide();
        $('#username_label').hide();
        $('#password_label').hide();
        $('#repository_label').hide();
    }
    if ($(this).val() == 'FTP') {
        $('#create_hostname').show();
        $('#create_port').show();
        $('#create_username').show();
        $('#create_password').show();
        $('#create_repository').show();
        $('#hostname_label').show();
        $('#port_label').show();
        $('#username_label').show();
        $('#password_label').show();
        $('#repository_label').show();
    }
});
$('#modal_storage').on('change', function () {
    if ($(this).val() == 'Local') {
        $('#modal_hostname').hide();
        $('#modal_port').hide();
        $('#modal_username').hide();
        $('#modal_password').hide();
        $('#modal_repository').hide();
        $('#hostname_label_modal').hide();
        $('#port_label_modal').hide();
        $('#username_label_modal').hide();
        $('#password_label_modal').hide();
        $('#repository_label_modal').hide();
    }
    if ($(this).val() == 'FTP') {
        $('#modal_hostname').show();
        $('#modal_port').show();
        $('#modal_username').show();
        $('#modal_password').show();
        $('#modal_repository').show();
        $('#hostname_label_modal').show();
        $('#port_label_modal').show();
        $('#username_label_modal').show();
        $('#password_label_modal').show();
        $('#repository_label_modal').show();
    }
});

function CreateOdooLink(){
    var link = $('#create_link').val();
    var storage = $('#create_storage').val();
    var hostname = $('#create_hostname').val();
    var port = $('#create_port').val();
    var username = $('#create_username').val();
    var password = $('#create_password').val();
    var repository = $('#create_repository').val();


    $.ajax({
        type: "POST",
        url: "/setting/general-file-protocol-create",
        dataType: "json",
        data: {
            link: link,
            storage: storage,
            hostname: hostname,
            port: port,
            username: username,
            password: password,
            repository: repository,

            csrfmiddlewaretoken: csrftoken,
        },
        success: function (data) {
            if (data == 'ok') {
                toastr.success('Informations Enregistrées');
                    location.reload();
            } 
            if (data.status == 'error') {
                toastr.error(data.error)
            }
        },
    });
}

function CreateEmailPnr(){
    var email = $('#email_pnr').val();
    var password = $('#email_pnr_password').val();

    $.ajax({
        type: "POST",
        url: "/setting/email-pnr-create",
        dataType: "json",
        data: {
            password: password,
            email: email,
            csrfmiddlewaretoken: csrftoken,
        },
        success: function (data) {
            if (data == 'ok') {
                toastr.success('Informations Enregistrées');
                    location.reload();
            } 
            if (data.status == 'error') {
                toastr.error(data.error)
            }
        },
    });

}

function CreateEmailNotif(){
    var email = JSON.stringify(finalMultiInsertTags[0])
    var value_name_id = $('#email_notif_value_name').val();

    $.ajax({
        type: "POST",
        url: "/setting/email-notification-recipients-create",
        dataType: "json",
        data: {
            value_name_id: value_name_id,
            email: email,
            csrfmiddlewaretoken: csrftoken,
        },
        success: function (data) {
            if (data == 'ok') {
                toastr.success('Informations Enregistrées');
                    location.reload();
            } 
            if (data.status == 'error') {
                toastr.error(data.error)
            }
        },
    });

}

function CreateEmailNotifSender(){
    var value_name_id = $('#email_notif_sender_value_name').val();
    var port = $('#port_email_notif_sender').val();
    var smtp = $('#smtp_email_notif_sender').val();
    var email = $('#email_notif_sender').val();
    var password = $('#password_email_notif_sender').val();

    $.ajax({
        type: "POST",
        url: "/setting/email-notification-sender-create",
        dataType: "json",
        data: {
            port:port,
            smtp:smtp,
            password: password,
            value_name_id: value_name_id,
            email: email,
            csrfmiddlewaretoken: csrftoken,
        },
        success: function (data) {
            if (data == 'ok') {
                toastr.success('Informations Enregistrées');
                    location.reload();
            } 
            if (data.status == 'error') {
                toastr.error(data.error)
            }
        },
    });

}

function AddEmailNotification() {
    $('.card.EmailNotifCard').show();
}

function CreateEmailFeeSender(){
    var email = $('#email_fee_sender').val();
    var password = $('#password_email_fee_sender').val();
    var smtp = $('#smtp_email_fee_sender').val();
    var port = $('#port_email_fee_sender').val();
    var config_id = $('#value_name_email_fee_sender').val();

    $.ajax({
        type: "POST",
        url: "/setting/email-fee-sender-create",
        dataType: "json",
        data: {
            email: email,
            password: password,
            smtp: smtp,
            port: port,
            config_id :config_id,
            csrfmiddlewaretoken: csrftoken,
        },
        success: function (data) {
            if (data == 'ok') {
                toastr.success('Informations Enregistrées');
                    location.reload();
            } 
            if (data.status == 'error') {
                toastr.error(data.error)
            }
        },
    });
}

$(document).ready(function () {
    $('#add-pnr-parsing').click(function () {
        
        document.getElementById('add-pnr-config-card').hidden=false;
    });

    $('#add-zenith-parsing-card select').on('change', function() {
    var value_name = $(this).val();
    console.log(value_name);
    });

});

// ---------------------------- All Parsing Functions ---------------------------



function CreateParsing(chemin,id) {
    const card = document.querySelector('#'+id);
    const select = card.querySelector("select")

    const value_name = $('#' + id + ' select').val();
    var value = JSON.stringify(finalMultiInsertTags[0])
    $.ajax({
        type: "POST",
        url: "/setting/"+chemin,
        dataType: "json",
        data: {
            value_name: value_name,
            value: value,
            csrfmiddlewaretoken: csrftoken,
        },
        success: function (data) {
            if (data == 'ok') {
                toastr.success('Informations Enregistrées');
                location.reload();
            } 
            if (data.status == 'error') {
                toastr.error(data.error)
            }
        },
    });

}

function HideCard(id){
    document.getElementById(id).hidden = true
}

function OpenCard(id){
    document.getElementById(id).hidden = false
}

function Emd_statues_update_show(){
    $('#emd_statues').hide();
    document.getElementById("emd_statues_update").hidden = false;
    document.getElementById("emd_statues_footer").hidden = false;

}

function UpdateEmdStatues(){
    var content = document.querySelector("#emd_statues_update");
    let statues = {};
    content.querySelectorAll("li").forEach(element => {
        let key = element.querySelector('.key').value;
        let value = element.querySelector('.value').value;
        statues[key] = value;
    });

    $.ajax({
        type: "POST",
        url: "/setting/emd-statues-update",
        dataType: "json",
        data: {
            statues: JSON.stringify(statues), 
            csrfmiddlewaretoken: csrftoken,
        },
        success: function (data) {
            if (data == 'ok') {
                toastr.success('Informations Modifiées');
                    location.reload();
            } 
            if (data.status == 'error') {
                toastr.error(data.error)
            }
        },
    });

}

function showPassword(inputId){
    var passwordInput = document.getElementById(inputId)

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
    } else {
        passwordInput.type = 'password';
    }
}



document.addEventListener('DOMContentLoaded', function () {
    var passwordFields = document.getElementsByClassName("passwordconfig");
    for (var i = 0; i < passwordFields.length; i++) {
        var maskedPassword = "*".repeat(passwordFields[i].textContent.length);
        passwordFields[i].textContent = maskedPassword;
    }
});
const CustomerNameInput = document.getElementById('customer-name-int-input');
const CustomerAddressInput = document.getElementById('customer-address-int-input');
const CustomerAddress2Input = document.getElementById('customer-address-2-int-input');
const CustomerFirstNameInput = document.getElementById('customer-firstname-int-input');
const CustomerCountryInput = document.getElementById('customer-country-int-input');
const CustomerCityInput = document.getElementById('customer-city-int-input');
const CustomerTypeInput = document.getElementById('customer-type-int-input');
const CustomerCompanyInput = document.getElementById('customer-company-int-input');
const CustomerList = document.getElementById('customer-list');
const ModalCustomer = document.getElementById('add-customer');
const CustomerZipCode = document.getElementById('customer-code-postal-input');
const SelectCustomerZipCode = document.querySelector('select#customer-code-postal-input')
const CustomerDepartement = document.getElementById('customer-departement-input');
const SelectCustomerCityInput = document.querySelector('select#customer-city-int-input');
const SelectCustomerDepartement = document.querySelector('select#customer-departement-input');
const CustomerEmail = document.getElementById('customer-mail-input');
const CustomerPhone = document.getElementById('customer-phone-input');

const CustomerSaveButton = document.getElementById('save-customer-button');
const customerSaveForm = document.getElementById('customerSaveForm')

const isInputNumber = (e) => {
    // Transform CharCode to String
    var char = String.fromCharCode(e.which);

    // If the character is not a number then we block the entry
    if(!(/[0-9]/.test(char))) {
        e.preventDefault()
    }
}

// Block block the input of the string 
CustomerZipCode.addEventListener("keypress", (e) => {
    isInputNumber(e)
})

CustomerTypeInput.addEventListener('change', (e)=> {
    CustomerFirstNameInput.toggleAttribute('required');
    CustomerNameInput.toggleAttribute('required');
})

CustomerSaveButton.setAttribute("disabled", true)

const checkFormInputs = (type) => {
    let name        = CustomerNameInput.value.trim()
    let firstname   = CustomerFirstNameInput.value.trim()
    let address     = CustomerAddressInput.value.trim()
    let email       = CustomerEmail.value.trim()
    let phone       = CustomerPhone.value.trim()
    let country     = CustomerCountryInput.value.trim()
    let city        = CustomerCityInput.value.trim() || SelectCustomerCityInput.value.trim()
    let company     = CustomerCompanyInput.value.trim()
    let zipCode     = CustomerZipCode.value.trim()
    let departement = CustomerDepartement.value.trim() || SelectCustomerDepartement.value.trim()

    if (type == "Particulier") {
        checkEachInput(name, CustomerNameInput)
        checkEachInput(firstname, CustomerFirstNameInput)
        checkEachInput(address, CustomerAddressInput)
        checkEachInput(email, CustomerEmail)
        checkEachInput(phone, CustomerPhone)
        checkEachInput(country, CustomerCountryInput)
        checkEachInput(city, CustomerCityInput || SelectCustomerCityInput)
        // checkEachInput(zipCode, CustomerZipCode)
        checkEachInput(departement, CustomerDepartement || SelectCustomerDepartement)

        if ([name, firstname, address, email, phone, city, country, departement].includes('')) {
            return false
        } else {
            return true
        }
    } else {
        checkEachInput(address, CustomerAddressInput)
        checkEachInput(email, CustomerEmail)
        checkEachInput(phone, CustomerPhone)
        checkEachInput(country, CustomerCountryInput)
        checkEachInput(city, CustomerCityInput || SelectCustomerCityInput)
        checkEachInput(company, CustomerCompanyInput)
        // checkEachInput(zipCode, CustomerZipCode)
        checkEachInput(departement, CustomerDepartement || SelectCustomerDepartement)

        if([address, email, phone, country, company, city, departement].includes('')) {
            return false
        } else {
            return true
        }  
    }
}

const setErrorFor = (input) => {
    input.classList.add("is-invalid");
    input.classList.remove("is-valid");
}

const setSuccessFor = (input) => {
    input.classList.add("is-valid");
    input.classList.remove("is-invalid");
}

const checkEachInput = (inputValue, inputName) => {
    if (inputValue === '')  {
        setErrorFor(inputName) 
        return 0
    } else {
        setSuccessFor(inputName)
        return 1
    }
}

customerSaveForm.addEventListener('change', () => {
    checkFormInputs(CustomerTypeInput.value) ? CustomerSaveButton.removeAttribute("disabled") : CustomerSaveButton.setAttribute("disabled", true)
})

CustomerSaveButton.addEventListener('click', (e) => {
    e.preventDefault();
    console.log('Button clickedddd!!!!!');
    $.ajax({
        type: 'POST',
        url: '/home/pnr/create-customer/',
        dataType: 'json',
        data: {
            Name : CustomerNameInput.value.trim(),
            FirstName: CustomerFirstNameInput.value.trim(),
            Address: CustomerAddressInput.value,
            Address_2: CustomerAddress2Input.value,
            Email: CustomerEmail.value,
            Phone: CustomerPhone.value,
            Country: CustomerCountryInput.value,
            City: CustomerCityInput.value || SelectCustomerCityInput.value,
            Type: CustomerTypeInput.value,
            Company: CustomerCompanyInput.value,
            Code_postal: CustomerZipCode.value || SelectCustomerZipCode.value,
            Departement: CustomerDepartement.value || SelectCustomerDepartement.value,
            csrfmiddlewaretoken: csrftoken,
        },
        success: (response) => {
            console.log('AJAX success entered');
            console.log(response);
            if (response.exist == 0) {
                CustomerList.innerHTML += `
                    <option value=${response.customer_id} selected="true"> ${response.intitule} </option> 
                `

                // Add the created customer to select2 list container
                // customerModificationSelectionList.innerHTML += `
                //     <option value=${response.customer_id} selected="true"> ${response.intitule} </option> 
                // `;

                toastr.info('Client créé avec succès!');

                $('#add-customer').modal('hide');
            }

            else if (response.exist == 1) {
                toastr.warning(`Le client ${response.intitule} existe déjà veuillez modifier le nom ou le prénom.`)
            }
            
        },
        error: (response) => {
            console.log(response);
        }
    })
})


//======= REMOVE ALL BUTTON CUSTOMER WITH INDEX GREATER THAN 0 ========//
// Because when you tried to get passenger data, we need to loop to get it
// And the length of buttonAddCustomer will be greater than 0
const buttonAddCustomer = document.querySelectorAll("#buttonAddCustomer");

if (buttonAddCustomer != []) {
    const modalCreateCustomerName      = document.getElementById('customer-name-int-input')
    const modalCreateCustomerFirstName = document.getElementById('customer-firstname-int-input')
    const modalCreateCustomerMail      = document.getElementById('customer-mail-input')
    const modalCreateCustomerPhone     = document.getElementById('customer-phone-input')
    if (buttonAddCustomer[0].getAttribute("data-passenger-informations") == "None") {
        if (modalCreateCustomerName != null && modalCreateCustomerFirstName != null && modalCreateCustomerMail != null && modalCreateCustomerPhone != null) {
            modalCreateCustomerName.value      = '';
            modalCreateCustomerFirstName.value = '';
            modalCreateCustomerMail.value      = '';
            modalCreateCustomerPhone.value     = '';
        }
    } else {
        const passengerInformations = JSON.parse(buttonAddCustomer[0].getAttribute("data-passenger-informations"));
        if (modalCreateCustomerName != null && modalCreateCustomerFirstName != null && modalCreateCustomerMail != null && modalCreateCustomerPhone != null) {
            modalCreateCustomerName.value      = passengerInformations.name || '';
            modalCreateCustomerFirstName.value = passengerInformations.surname || '';
            modalCreateCustomerMail.value      = passengerInformations.email[0] || '';
            modalCreateCustomerPhone.value     = passengerInformations.phone[0] || '';
        }
    }
}
//====================================================================//


//========== CLEAR ALL INPUTS FIELDS =============//
const modalCreateCustomerName       = document.getElementById('customer-name-int-input')
const modalCreateCustomerFirstName  = document.getElementById('customer-firstname-int-input')
const modalCreateCustomerMail       = document.getElementById('customer-mail-input')
const modalCreateCustomerPhone      = document.getElementById('customer-phone-input')
const modalCreateCustomerAddress1   = document.getElementById('customer-address-int-input')
const modalCreateCustomerAddress2   = document.getElementById('customer-address-2-int-input')

const buttonClearInputFields        = document.getElementById('buttonClearInputFields') 

if (buttonClearInputFields != null) {
    buttonClearInputFields.addEventListener("click", (e) => {
        e.preventDefault()
    
        modalCreateCustomerName.value      = '';
        modalCreateCustomerFirstName.value = '';
        modalCreateCustomerMail.value      = '';
        modalCreateCustomerPhone.value     = '';
        modalCreateCustomerAddress1.value  = '';
        modalCreateCustomerAddress2.value  = '';
    })
}
//================================================//

const customerModificationValidate = document.getElementById('customer-modification-validate')

if (customerModificationValidate != null) {
    customerModificationValidate.addEventListener('click', (e)=> {
        const Email = document.querySelector('[name="input-modify-customer-email"]');
        const Telephone = document.querySelector('[name="input-modify-customer-telephone"]');
        const Address1 = document.querySelector('[name="input-modify-customer-address1"]');
        const Address2 = document.querySelector('[name="input-modify-customer-address2"]');
        const CodePostal = document.querySelector('[name="input-modify-customer-code-postal"]');
        const City = document.querySelector('[name="input-modify-customer-city"]');
        const Department = document.querySelector('[name="input-modify-customer-department"]');
        const Country = document.querySelector('[name="input-modify-customer-country"]');
        const id_input = document.querySelector(".selected-customer-id");
        $.ajax({
            type: 'POST',
            url: '/home/pnr/modify-customer/',
            dataType: 'json',
            data: {
                Address: Address1.value,
                Address_2: Address2.value,
                Email: Email.value,
                Phone: Telephone.value,
                Country: Country.value,
                City: City.value,
                Code_postal: CodePostal.value,
                Departement: Department.value,
                Id: id_input.value,
                csrfmiddlewaretoken: csrftoken,
            },
            success: (response) => {
                console.log(response);
                $('#edit-customers').modal('hide');
                location.reload();
                toastr.info('Client modifié!');
            },
            error: (response) => {
                console.log(response);
            }
        })
    });
}


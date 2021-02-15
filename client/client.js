/*
    Programmatic client for loans server
    Anna Rekow

    to run: node client.js
*/
// *****************************
const fetch = require("node-fetch");
// const LOAN_API_URL = 'http://127.0.0.1:5000/loans';
const LOAN_API_URL = 'http://ec2-18-221-55-247.us-east-2.compute.amazonaws.com/loans';


async function create(data) {
    /* creates loan object

        data: js object w loan params
    */
    const res = await fetch(LOAN_API_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    const json = await res.json();
    console.log(json);
}

async function get(url) {
    /* logs/returns all or one loan object

        for all loans, url: LOAN_API_URL
        for loan n: LOAN_API_URL + '/n'
    */
    const res = await fetch(url);
    const json = await res.json();
    console.log(json);
}

async function update(url, data) {
    /* updates loan object

        url must contain LOAN_API_URL + '/n'
    */
    const res = await fetch(url, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    const json = await res.json();
    console.log(json);
}



// ******* TEST ******** //


const data = { 
    "amount": 100.0, 
    "interest_rate": 0.5, 
    "length_in_months": 12, 
    "monthly_payment": 10.0 
}
const data_update = { 
    "amount": 1000000.0
}
create(data);
update(LOAN_API_URL + '/1', data_update);
get(LOAN_API_URL);


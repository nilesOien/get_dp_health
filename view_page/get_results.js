
// Clear results
function clear_results(){
  document.getElementById('result_para').innerHTML = '';
  return;
}

// Show options for provider/source/instrument
async function show_options(){
  const url='/dp-health-options';

  let response = await fetch(url);

  if (!response.ok) {
    alert(response.statusText);
    return;
  }

  let responseText = await response.text();

  try {
    responseObj = JSON.parse(responseText);
  } catch (error) {
    alert("Error parsing JSON from " + url + " : " + responseText, error.message);
    return;
  }

  h='<table><tr><th>Provider</th><th>Source</th><th>Instrument</th></tr>';
  for (const item of responseObj){
     h += '<tr><td>' + item.provider + '</td><td>' + item.source + '</td><td>' + item.instrument + '</td></tr>';
  }
  h += '</table>';
  const para = document.getElementById('result_para');
  para.innerHTML=h;

  return;
}

// Tell the user about what we found, wether we got it via GET or POST
function put_results(responseObj, method){

  const para = document.getElementById('result_para');

  h='The response using ' + method + ':<br>';
  for (const [key, value] of Object.entries(responseObj)) {
    h += '<b>' + key + '</b> : ' + value + '<br>';
  }
  para.innerHTML = h;

  return;
}

// Use POST to fetch results
async function get_results_post(provider, source, instrument){

   const url='/get-dp-health-post';

   payload = {'provider': provider, 'source': source, 'instrument': instrument};
   try {
   const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', // We are sending JSON
        'Accept': 'application/json'        // We expect JSON back
      },
      body: JSON.stringify(payload)
    });

    // Check if the response status is 200-299
    if (!response.ok) {
      alert(`HTTP error! Status: ${response.status}`);
      return;
    }

    const jsonResponse = await response.json(); // Parses the returning JSON data
    put_results(jsonResponse, 'POST');
    } catch (error) {
     
       alert('Error during POST request:', error);
       return;
    }
   return;
}


// Use GET to fetch results
async function get_results_get(provider, source, instrument){
  const url='/get-dp-health-get?provider=' + provider + '&source=' + source + '&instrument=' + instrument;

  let response = await fetch(url);

  if (!response.ok) {
    alert(response.statusText);
    return;
  }

  let responseText = await response.text();

  try {
    responseObj = JSON.parse(responseText);
  } catch (error) {
    alert("Error parsing JSON from " + url + " : " + responseText, error.message);
    return;
  }
  put_results(responseObj, 'GET');
  return;
}

// This just fetches values, then looks to see if we want to use POST or GET and then does that
function get_results(){

  const provider = document.getElementById('provider_box').value;
  const source = document.getElementById('source_box').value;
  const instrument = document.getElementById('instrument_box').value;
  const use_post = document.getElementById('use_post').checked;

  if(use_post){
    get_results_post(provider, source, instrument);
  } else {
    get_results_get(provider, source, instrument);
  }

  return;
}


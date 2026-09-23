
// Clear results
function clear_results(){
  document.getElementById('result_para').innerHTML = '';
  return;
}


// Tell the user about what we found, wether we got it via GET or POST
function put_results(responseObj){

  const para = document.getElementById('result_para');

  h='';
  for (const [key, value] of Object.entries(responseObj)) {
    h += '<b>' + key + '</b> : ' + value + '<br>';
  }
  para.innerHTML = h;

  return;
}

// Use POST to fetch results
async function get_results_post(source, instrument){

   const url='/get-dp-health-post';

   payload = {'source': source, 'instrument': instrument};
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
    put_results(jsonResponse);
    } catch (error) {
     
       alert('Error during POST request:', error);
       return;
    }
   return;
}


// Use GET to fetch results
async function get_results_get(source, instrument){
  const url='/get-dp-health-get?source=' + source + '&instrument=' + instrument;

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
  put_results(responseObj);
  return;
}

// This just fetches values, then looks to see if we want to use POST or GET and then does that
function get_results(){

  const source = document.getElementById('source_box').value;
  const instrument = document.getElementById('instrument_box').value;
  const use_post = document.getElementById('use_post').checked;

  if(use_post){
    get_results_post(source, instrument);
  } else {
    get_results_get(source, instrument);
  }

  return;
}


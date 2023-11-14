<script lang="ts">
  import EventCard from '$lib/components/eventCard.svelte';
  import type { _Event } from '$lib/types/event';

  let showForm = true;
  let hasError: boolean = false;

  let locationName: string = "Melbourne Australia"

  let startDate: string, endDate: string = '';

  let page: number = 0;

  let events: _Event[] = [];

  const fetchData = async(page: number) => {
    const endpoint = 'http://localhost:8080/api/event/';
    const data = {
      location_name: locationName,
      start_datetime: startDate,
      end_datetime: endDate,
      page,
    };

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const responseData = await response.json();
      console.log("Response from backend:", responseData);
      events = [...responseData['events']];
      showForm = false;
    } catch (error) {
      hasError = true;
      console.log(error);
    }
  
  }

  const submitForm = async () => {
    page = 0;
    fetchData(page);
  };

  const nextPage = () => {
    page++;
    fetchData(page);
  };
  

</script>

{#if showForm}
  <div class={hasError ? "flex flex-col items-center justify-center h-screen bg-grey-600 border-4 border-red-500" : "flex flex-col items-center justify-center h-screen bg-grey-600"}>
    <div class="mb-4">
      <label for="locationName" class="block text-gray-700 text-sm font-bold mb-2">Location Name</label>
      <input type="text" id="locationName" bind:value={locationName} class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" />
    </div>

    <div class="mb-4">
      <label for="startDate" class="block text-gray-700 text-sm font-bold mb-2">Start Date Time</label>
      <input type="datetime-local" id="startDate" bind:value={startDate} class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" />
    </div>

    <div class="mb-6">
      <label for="endDate" class="block text-gray-700 text-sm font-bold mb-2">End Date Time</label>
      <input type="datetime-local" id="endDate" bind:value={endDate} class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" />
    </div>

    <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="button" on:click={submitForm}>
      Submit
    </button>
  </div>
{/if}

{#if !showForm}
  <div class="flex flex-col items-center justify-start h-screen overflow-auto">
    <div class="w-full flex justify-between items-center p-4">
      <button 
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
        on:click={() => showForm = true}
      >
        Back
      </button>
      <h3 class="text-xl font-bold">Events</h3>
      <button 
        class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
        on:click={nextPage}
      >
        Next
      </button>
    </div>
    {#each events as event}
      <EventCard {event} />
    {/each}
  </div>
{/if}

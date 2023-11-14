<script lang="ts">
  import type { _Event } from '$lib/types/event';

  export let event: _Event;
</script>

<div class="max-w-sm rounded overflow-hidden shadow-lg m-2 bg-white mb-4 h-auto min-h-[200px] flex flex-col justify-between hover:bg-gray-200 transition-colors duration-300">
 
  <div class="px-6 py-4">
    <div class="font-bold text-xl mb-2">{event.name}</div>
    <p class="text-gray-700 text-base">
      Type: {event.type}
    </p>
    <p class="text-gray-700 text-base">
      ID: {event.id}
    </p>
    <p class="text-gray-700 text-base">
      Test Event: {event.test ? 'Yes' : 'No'}
    </p>
    <p class="text-gray-700 text-base">
      Locale: {event.locale}
    </p>
  </div>
</div>

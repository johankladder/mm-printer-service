<template>
  <div id="app">

    <div class="m-8">

      <!-- Options section -->
      <div>
        <div class="flex mb-2">
          <b><i>Options</i></b>
        </div>
        <div class="grid grid-cols-4 gap-4">
          <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Restart server
          </button>

          <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Clear all jobs
          </button>
        </div>

      </div>

      <!-- Printer section -->
      <div class="mt-8">
        <div class="flex mb-2">
          <b><i>Printers</i></b>
        </div>
        <div class="text-white grid grid-cols-3 gap-4">
          <div :key="printer" v-for="printer in printers"
            class="flex grid grid-rows-3 aspect-square bg-slate-800 rounded-lg p-4">
            <div class="">
              Printer {{ printer }}
            </div>


            <div class="flex items-center justify-center grow ">
              <div v-if="isPrinterProcessing(printer)" class="flex items-center justify-center grow ">
                <svg aria-hidden="true" class="w-8 h-8 mr-2 text-white-200 animate-spin dark:text-gray-600 fill-blue-600"
                  viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path
                    d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                    fill="currentColor" />
                  <path
                    d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                    fill="currentFill" />
                </svg>
              </div>
            </div>

            <div class="flex items-end justify-center ">
              <button class="items-end bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                Clear jobs
              </button>
            </div>
          </div>
        </div>
      </div>



      <!-- Console section -->
      <div class="mt-8">
        <div class="flex mb-2">
          <b><i>Console</i></b>
        </div>
        <div class="console-container bg-slate-800 overflow-auto p-4 text-white rounded-lg">
          <div>
            <div class="flex" :key="subscription" v-for="subscription in Object.keys(subscriptions)">
              {{ subscription }} {{ subscriptions[subscription] }}
            </div>
            <div v-if="Object.keys(subscriptions).length == 0">
              <i>Nothing to show..</i>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import mqtt from "mqtt/dist/mqtt";


export default {
  name: 'App',
  components: {

  },

  data() {
    return {
      printers: [1, 2, 3, 4, 5, 6, 7],
      subscriptions: {}
    }
  },

  mounted() {
    var client = mqtt.connect('mqtt://localhost', {
      port: 9001
    });

    client.on('connect', function () {
      client.subscribe('mm/printing/status/+')
    })

    client.on('message', (topic, payload) => {
      this.subscriptions[topic] = JSON.parse(new TextDecoder().decode(payload));
    })
  },


  methods: {

    isPrinterProcessing(printerId) {
      let values = Object.keys(this.subscriptions).filter((entry) => {
        let payload = this.subscriptions[entry]
        return payload.printer.id == printerId && payload.status == "PROCESSING"
      })
      return values.length > 0
    }

  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.console-container {
  height: 200px;

}
</style>

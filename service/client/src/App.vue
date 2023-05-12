<template>
  <div id="app">

    <div class="m-8 ">
      <div class="flex">
        <div class="grow" v-on:click="onToggleConsole()">
          <div v-if="mqttConnected" class="bg-green-200 p-4 rounded-xl shadow-lg">
            <div class="font-bold text-xl">
              <i>Printserver online!</i>
            </div>
            <i>{{ beatifyDate(lastConnectionPublish) }} </i>
          </div>
          <div v-else class="bg-red-500 p-4 rounded-lg text-white shadow-lg font-bold text-xl">
            Niet online - wacht voor verbinding. Printers werken mogelijk nog niet
          </div>
        </div>
      </div>

      <!-- Printer section -->
      <div class="mt-8" v-if="printers.length > 0">
        <div class=" grid grid-cols-3 xl:grid-cols-6 gap-4">
          <div :key="printer" v-for="printer in printers"
            class="shadow-lg flex grid aspect-square bg-slate-800 rounded-lg p-4">
            <div class="flex overflow-hidden truncate text-3xl  text-white">
              <div class="font-bold">
                <b>{{ beautifyPrinterName(printer) }}</b>
              </div>
    
            </div>
            <div class="flex items-center justify-center text-xl">
              <div v-if="retrievePrinterStatus(printer) == 4" class="flex items-center justify-center grow text-white ">
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
              <div v-else-if="retrievePrinterStatus(printer) == 3" class="bg-green-200 p-4 rounded-xl ">
                <div class="font-bold">
                  <i>Online</i>
                </div>
                <i class="text-sm">{{ retrieveLatestPrinterStatusTime(printer) }}</i>
              </div>
              <div v-else-if="retrievePrinterStatus(printer) == undefined" class="bg-yellow-400 p-4 rounded-xl font-bold  animate-pulse">
                Printer status ophalen...
              </div>
              <div v-else class="bg-red-500 p-4 rounded-xl font-bold text-white animate-pulse">Error ({{
                retrievePrinterStatus(printer) }})</div>
            </div>

            <div class="flex justify-between items-end">
              <div>
                <button v-on:click="onTestPage(printer)" v-if="retrievePrinterStatus(printer) == 3"
                  class="items-end bg-slate-500 hover:bg-blue-700 text-white font-bold py-4 px-4 rounded-xl grow">
                  Test page
                </button>
              </div>
              <div>
                <button v-on:click="onClearAllJobs(printer)"
                  class="items-end bg-slate-500 hover:bg-blue-700 text-white font-bold py-4 px-4 rounded-xl grow">
                  Clear jobs
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>


      <!-- Console section -->
      <div class="mt-8" v-if="printers.length > 0">
        <div v-if="showConsole" class="mb-4">
          <div class="console-container bg-slate-800 overflow-auto p-4 text-white rounded-lg shadow-lg">
            <div>
              <div class="flex" :key="subscription" v-for="subscription in consoleSubscriptions">
                {{ subscription.time }} {{ subscription.topic }} {{ subscription.payload }}
              </div>
              <div v-if="consoleSubscriptions.length == 0">
                <i>Nothing to show..</i>
              </div>
            </div>
          </div>
        </div>
        <div class="space-x-4" v-if="showConsole">
          <button v-on:click="onToggleConsole()"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-4 px-4 rounded-xl text-xl shadow-lg">
            Show console
          </button>
          <button v-on:click="onRestartServer()"
            class=" bg-blue-500 hover:bg-blue-700 text-white font-bold py-4 px-4 rounded-xl text-xl shadow-lg">
            Restart server
          </button>

          <button v-on:click="onClearAllJobs()"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-4 px-4 rounded-xl text-xl shadow-lg">
            Clear all jobs
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import mqtt from "mqtt/dist/mqtt";
import axios from 'axios'


export default {
  name: 'App',

  data() {
    return {
      mqttConnected: false,
      lastConnectionPublish: null,
      connectionTimer: null,
      printers: [],
      subscriptions: {},
      consoleSubscriptions: [],
      printerStatuses: {},
      showConsole: false
    }
  },

  mounted() {

    var client = mqtt.connect('mqtt://' + process.env.VUE_APP_MQTT_HOST, {
      port: 9001
    });

    client.on('connect', function () {
      client.subscribe('mm/printing/status/+')
      client.subscribe('mm/mqtt/printing/status')
      client.subscribe('mm/printing/printer/status/+')
    })

    client.on('message', (topic, payload) => {
      if (topic.startsWith('mm/printing/status')) {
        this.handlePrintStatusSubscription(topic, payload)
      } else if (topic.startsWith('mm/mqtt/printing/status')) {
        this.handlePrintServiceStatus()
        this.onSyncPrinters()
      } else if (topic.startsWith('mm/printing/printer/status/')) {
        this.handlePrinterStatusSubscription(topic, payload)
      }
    })

    this.startConnectionTimer()
    this.onSyncPrinters();

  },

  beforeUnmount() {
    clearTimeout(this.connectionTimer)
  },

  methods: {

    startConnectionTimer() {
      this.connectionTimer = setTimeout(() => {
        if (this.lastConnectionPublish) {
          let diffMs = (new Date()) - this.lastConnectionPublish
          let seconds = Math.floor((diffMs / 1000));
          if (seconds > 60) {
            this.mqttConnected = false
          }
        }
        this.startConnectionTimer()
      }, 6000)
    },

    handlePrinterStatusSubscription(topic, payload) {
      let data = JSON.parse(new TextDecoder().decode(payload));
      let printerName = topic.split('/')[4]
      this.printerStatuses[printerName] = {
        status: data.status,
        latestPing: new Date()
      }
    },

    retrievePrinterStatus({ queue_name }) {
      if (!this.printerStatuses[queue_name]) {
        return undefined
      }
      return this.printerStatuses[queue_name].status
    },

    retrieveLatestPrinterStatusTime({ queue_name }) {
      if (!this.printerStatuses[queue_name]) {
        return undefined
      }
      return this.beatifyDate(this.printerStatuses[queue_name].latestPing);
    },

    beatifyDate(date) {
      return date.toLocaleDateString('nl', { hour: "numeric", minute: "numeric", second: "numeric" })
    },

    beautifyPrinterName({ queue_name }) {
      const arr = queue_name.replaceAll('_', ' ').split(" ");
      for (var i = 0; i < arr.length; i++) {
        arr[i] = arr[i].charAt(0).toUpperCase() + arr[i].slice(1);

      }
      return arr.join(" ");
    },


    handlePrintStatusSubscription(topic, payload) {
      this.subscriptions[topic] = JSON.parse(new TextDecoder().decode(payload));
      let now = new Date(Date.now())
      this.consoleSubscriptions.unshift({
        "time": now.toUTCString(),
        "topic": topic,
        "payload": JSON.parse(new TextDecoder().decode(payload))
      })
      if (this.consoleSubscriptions.length > 100) {
        this.consoleSubscriptions.pop()
      }
    },

    handlePrintServiceStatus() {
      this.mqttConnected = true
      this.lastConnectionPublish = new Date()
    },

    onRestartServer() {
      axios.post(process.env.VUE_APP_FLASK_HOST + "/server/restart")
    },

    onClearAllJobs(printer) {
      if (!printer) {
        axios.post(process.env.VUE_APP_FLASK_HOST + "/cups/cancel-all-jobs")
      } else {
        axios.post(process.env.VUE_APP_FLASK_HOST + "/cups/cancel-jobs", {
          'queue_name': printer.queue_name
        })
      }
    },

    onTestPage(printer) {
      axios.post(process.env.VUE_APP_FLASK_HOST + "/cups/test-page", {
        'queue_name': printer.queue_name
      })
    },

    onSyncPrinters() {
      axios.get(process.env.VUE_APP_FLASK_HOST + "/cups/printers")
        .then(({ data }) => this.printers = data)
    },

    onToggleConsole() {
      this.showConsole = !this.showConsole
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
  white-space: nowrap;

}
</style>

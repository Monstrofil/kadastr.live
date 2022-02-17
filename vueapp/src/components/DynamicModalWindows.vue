<template>
  <template v-for="child in modalWindows" :key="child.component.name">
    <component :is="child.component" v-bind="child.props"></component>
  </template>
</template>
<script>
import ModalWindow from "@/components/ModalWindow";

export default {
  name: 'DynamicModalWindows',
  data() {
    return {
      modalWindows: [],
      modalId: 0
    }
  },
  methods: {
    openDialog(modalWindow, props) {
      const modalId = this.modalId++;
      this.modalWindows.push({
        component: modalWindow,
        id: modalId,
        props: {windowId: modalId, ...props}

      })
    },
    closeDialog(window) {
      this.modalWindows = this.modalWindows.filter((item) => {
        return item.id !== window.windowId
      })
    },
    openYesNoDialog(header, content, onAgree, onReject) {
      const modalId = this.modalId++;
      this.modalWindows.push({
        component: ModalWindow,
        id: modalId,
        props: {
          header: header,
          content: content,
          windowId: modalId,
          onCloseFunc: (window, result) => {
            if(result === 'yes') {
              onAgree()
            }
            else {
              onReject()
            }
            this.closeDialog(window);
          }
        }
      })
    }
  }
}
</script>
<style scoped>

table.route_list th {
  font-weight: normal;
  font-size: 14px;
  color: #ffffff;
  background-color: #354251;
}

table.route_list td {
  font-size: 13px;
  color: #354251;
}

table.route_list td, table.route_list th {
  white-space: pre-wrap;
  padding: 10px 2px;
  line-height: 13px;
  vertical-align: middle;
  border: 1px solid #354251;
}

table.route_list tr:hover {
  background-color: #f9fafb
}

table.route_list tr:hover td {
  color: #354251;
  cursor: default;
}

</style>
<style scoped>
h3 {
  margin: 40px 0 0;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
<template>
  <div ref="element" class="mapboxgl-ctrl">

    <div v-if="false && updatesInfo" class="calendarContainer">
      <div class="calendarDate">
        <i class="fa fa-chevron-left slideRevision slideRevisionBack"
           :class="{'disabled': currentUpdate === updatesInfo.length - 1}"
           @click="slideRevisionBack"></i>



        <span class="dateText" v-tooltip="{ content: tooltipText, html: true }">{{ formatDate(updatesInfo[currentUpdate].created_at) }}</span>

        <i class="fa fa-chevron-right slideRevision slideRevisionForward"
           :class="{'disabled': currentUpdate === 0}"
           @click="slideRevisionForward"></i>

        <h6><span class="badge bg-warning betaBadge" v-tooltip="{ content: tooltipText, html: true }">Beta</span></h6>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import moment from "moment";

export default {
  name: "WayBackMachine",
  data() {
    return {
      updatesInfo: null,
      currentUpdate: null,
      tooltipText: "Функція працює в тестовому режимі. <br><br>" +
          "Дозволяє обрати дату, згідно якої будуть відображені земельні ділянки. <br>" +
          "<b>Не впливає на інші слої, не впливає на завантаження.<b>"
    }
  },
  methods: {
    onAdd() {
      return this.$refs.element
    },
    onRemove() {

    },
    onInputEnd() {

    },
    formatDate(dateIsoString) {
      return moment(dateIsoString).format('DD.MM.YYYY');
    },
    emitRevisionChange(newRevisionIndex) {
      if (this.currentUpdate === newRevisionIndex) {
        return
      }

      this.currentUpdate = newRevisionIndex;
      if (this.currentUpdate !== 0) {
        this.$emit('revisionChanged', this.updatesInfo[this.currentUpdate]['id'])
      } else {
        this.$emit('revisionChanged', null)
      }
    },
    slideRevisionBack() {
      this.emitRevisionChange(Math.min(this.currentUpdate + 1, this.updatesInfo.length - 1))
    },
    slideRevisionForward() {
      this.emitRevisionChange(Math.max(this.currentUpdate - 1, 0))
    }
  },
  mounted() {
    axios.get(
        `/api/updates/`
    ).then(response => {
      this.updatesInfo = response.data;
      this.currentUpdate = 0;
    });
  }
}
</script>

<style lang="scss" scoped>
$waybackSlideHeight: 40px;

$betaBadgeOffsetLeft: 40px;
$betaBadgeOffsetTop: 5px;

.calendarContainer {
  // place for the beta badge
  margin-left: $betaBadgeOffsetLeft;
  margin-top: $betaBadgeOffsetTop;
}

.calendarDate {
  background-color: #fff;
  outline: none;
  height: $waybackSlideHeight;
  padding: 0 7px;
  width: 140px;
  border: none;
  font-family: inherit;
  color: #0288d1;
  border-radius: 25px;
  font-weight: 600;
  box-shadow: 0 1px 4px rgba(0, 0, 0, .3);
  position: relative;

  text-align: center;

  .dateText {
    line-height: $waybackSlideHeight;
    color: black;
    font-size: 10pt;
  }

  .slideRevision {
    font-size: 25pt;
    position: absolute;
    line-height: $waybackSlideHeight;
    cursor: pointer;

    &.slideRevisionBack {
      left: 5px;
    }

    &.slideRevisionForward {
      right: 5px;
    }

    &.disabled {
      color: #546d7c;
      cursor: not-allowed;
    }
  }

  .betaBadge {
    position: absolute;
    left: -$betaBadgeOffsetLeft;
    top: -$betaBadgeOffsetTop;
  }
}

</style>
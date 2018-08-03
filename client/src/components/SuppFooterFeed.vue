<template>
  <b-col md="6">
    <h5>{{ feedType }}
      <a class="" href="#" style="float: right;">View all</a>
    </h5>
    <b-list-group>
      <b-list-group-item
        v-for="(feed, index) in feeds"
        v-bind:key="index">
        <h3>
          <a class="" v-bind:href="feed.link">
            {{ feed.title }}
          </a>
        </h3>
      </b-list-group-item>
    </b-list-group>
  </b-col>
</template>

<script>
export default {
  name: 'SuppFooterFeed',
  props: {
    feedType: {
      type: String,
      required: true
    }
  },
  data () {
    return {
      feeds: [
        {
          title: 'abc',
          link: '#'
        }
      ]
    }
  }
}
</script>

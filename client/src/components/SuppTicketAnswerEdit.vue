<template>
  <div>
    <b-card>
      <form @submit.prevent="onSubmit">
        <div class="form-group row">
            <label for="answer" class="col-sm-2 col-form-label text-right">Answer</label>
            <div class="col-sm-8">
            <mavon-editor style="z-index:10;"
                          language="en"
                          defaultOpen="edit"
                          placeholder="Add your response to this ticket here..."
                          v-model="body"
                          v-bind:boxShadow=false
                          v-bind:toolbars="toolbars"
                          name="body"
                          v-validate="'required'"/>
            <span v-show="errors.has('body')" class="errors">{{ errors.first('body') }}</span>
            </div>
        </div>

        <div class="form-group row">
            <label for="assignee" class="col-sm-2 col-form-label text-right">Assigned to</label>
            <div class="col-sm-8">
              <Select2 name="assignee" v-model="assignee" :options="options" :settings="{ theme: 'bootstrap4' }"
                v-validate="'required'" :class="{ 'errors': errors.has('assignee')}"/>
              <span v-show="errors.has('assignee')" class="errors">{{ errors.first('assignee') }}</span>
            </div>
        </div>

        <div class="form-group row">
            <label for="ticketStatus" class="col-sm-2 col-form-label text-right">Ticket Status</label>
            <div class="col-sm-8">
              <b-form-select name="status" v-model="status" :options="statusOptions" class="mb-3"
                v-validate="'required'" :class="{ 'errors': errors.has('status')}"/>
              <span v-show="errors.has('status')" class="errors">{{ errors.first('status') }}</span>
            </div>
        </div>

        <div class="form-group row">
            <label for="privacy" class="col-sm-2 col-form-label text-right">Privacy</label>
            <div class="col-sm-8">
            <b-form-select v-model="privacy" :options="privacyOptions" class="mb-3" />
            </div>
        </div>

        <div class="form-group row">
            <label for="ticketSelect" class="col-sm-2 col-form-label text-right">Link URL</label>
            <div class="col-md-8">
            <div class="input-group mb-3">
                <div class="input-group-prepend">
                <span class="input-group-text" id="basic-addon1">
                    <icon name="link"></icon>
                    <icon name="info-circle" id="exButton2" style="margin-left:7px;"></icon>
                </span>
                </div>
                <input type="text" class="form-control" placeholder="Username" aria-label="Username" aria-describedby="basic-addon1">
                <b-tooltip target="exButton2" title="Include an outside link to any relevant details.!"></b-tooltip>
            </div>
            </div>
        </div>

        <div class="form-group row">
            <label for="ticketSelect" class="col-sm-2 col-form-label text-right">Send copy to</label>
            <div class="col-md-8">
            <div class="input-group mb-3">
                <div class="input-group-prepend">
                <span class="input-group-text" id="basic-addon1">
                    <icon name="envelope"></icon>
                    <icon name="info-circle" id="exButton2" style="margin-left:7px;"></icon>
                </span>
                </div>
                <input type="text" class="form-control" placeholder="Username" aria-label="Username" aria-describedby="basic-addon1">
                <b-tooltip target="exButton2" title="Include an outside link to any relevant details.!"></b-tooltip>
            </div>
            </div>
        </div>

        <div class="form-group row">
            <label for="assignee" class="col-sm-2 col-form-label text-right">Attachment</label>
            <div class="col-sm-8">
            <b-form-file v-model="file" plain></b-form-file>
            </div>
        </div>

        <div class="form-group row">
            <div class="offset-md-2 col-sm-8">
            <button type="submit" class="btn btn-primary">Post</button>
            <button type="submit" class="btn btn-danger">Close</button>
            </div>
        </div>
      </form>

    </b-card>
  </div>
</template>

<script>
import Vue from 'vue'
import mavonEditor from 'mavon-editor'
import {
  ANSWER_CREATE
} from '@/store/actions.type'
import 'mavon-editor/dist/css/index.css'

import 'vue-awesome/icons/info-circle'
import 'vue-awesome/icons/link'
import 'vue-awesome/icons/envelope'

import Select2 from 'v-select2-component'
import 'select2/dist/css/select2.css'
import 'select2-bootstrap4-theme/dist/select2-bootstrap4.css'

Vue.use(mavonEditor)
export default {
  name: 'SuppTicketAnswerEdit',
  components: {
    Select2
  },
  props: {
    ticketId: {
      type: Number,
      required: true
    }
  },
  data () {
    return {
      body: '',
      assignee: 1,
      options: [
        { id: 1, text: 'foo' },
        { id: 2, text: 'foo2' }
      ],
      status: '',
      statusOptions: [
        { value: '', text: 'Select a Status' },
        { value: 'new', text: 'New' },
        { value: 'assigned', text: 'Assigned' },
        { value: 'inprogress', text: 'In Progress' },
        { value: 'pending', text: 'Pending Input' },
        { value: 'closed', text: 'Closed' }
      ],
      privacy: '',
      privacyOptions: [
        { value: '', text: '---------' },
        { value: 'IH', text: 'Inherit' },
        { value: 'PU', text: 'Public' },
        { value: 'PR', text: 'Private' }
      ],
      toolbars: {
        bold: true,
        italic: true,
        header: true,
        quote: true,
        ol: true,
        ul: true,
        link: true,
        imagelink: true,
        code: true,
        table: true,
        fullscreen: true,
        help: true,
        subfield: true,
        preview: true
      },
      file: null
    }
  },
  methods: {
    onSubmit () {
      this.$validator.validate().then(result => {
        if (!result) {
          return
        }
        this.$store.dispatch(ANSWER_CREATE, {
          ticketId: this.ticketId,
          answer: {
            body: this.body,
            createdBy: this.assignee,
            // status: this.status,
            privacy: this.privacy
          }
        })
      })
    }
  }
}
</script>

<style>

</style>

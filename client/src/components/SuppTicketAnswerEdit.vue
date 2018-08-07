<template>
  <div>
    <b-card>
      <form>
        <div class="form-group row">
            <label for="answer" class="col-sm-2 col-form-label text-right">Answer</label>
            <div class="col-sm-8">
            <mavon-editor style="z-index:10;"
                            language="en"
                            defaultOpen="edit"
                            placeholder="Add your response to this ticket here..."
                            v-model="value"
                            v-bind:boxShadow=false
                            v-bind:toolbars="toolbars"/>
            </div>
        </div>

        <div class="form-group row">
            <label for="assignee" class="col-sm-2 col-form-label text-right">Assigned to</label>
            <div class="col-sm-8">
            <Select2 name="serverVersion" v-model="selected" :options="options" :settings="{ theme: 'bootstrap4' }"/>
            </div>
        </div>

        <div class="form-group row">
            <label for="ticketStatus" class="col-sm-2 col-form-label text-right">Ticket Status</label>
            <div class="col-sm-8">
            <b-form-select v-model="statusSelected" :options="statusOptions" class="mb-3" />
            </div>
        </div>

        <div class="form-group row">
            <label for="privacy" class="col-sm-2 col-form-label text-right">Privacy</label>
            <div class="col-sm-8">
            <b-form-select v-model="privacySelected" :options="privacyOptions" class="mb-3" />
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
  data () {
    return {
      value: '',
      selected: 1,
      options: [
        { id: 1, text: 'foo' },
        { id: 2, text: 'foo2' }
      ],
      statusSelected: null,
      statusOptions: [
        { value: null, text: 'Select a Status' },
        { value: 'new', text: 'New' },
        { value: 'assigned', text: 'Assigned' },
        { value: 'inprogress', text: 'In Progress' },
        { value: 'pending', text: 'Pending Input' },
        { value: 'closed', text: 'Closed' }
      ],
      privacySelected: null,
      privacyOptions: [
        { value: 'null', text: '---------' },
        { value: 'inherit', text: 'Inherit' },
        { value: 'public', text: 'Public' },
        { value: 'private', text: 'Private' }
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
  }

}
</script>

<style>

</style>

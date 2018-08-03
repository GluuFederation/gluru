<template>
  <footer>
    <b-container>
      <hr class="top-footer-line">
      <b-row>
        <b-col md="2">
          <div>
            <ul>
              <li><a href="http://www.gluu.org/company/our-story/" title="About Gluu">Company</a></li>
              <li><a href="http://www.gluu.org/partners/overview/" title="Gluu Partners">Partners</a></li>
              <li><a href="http://www.gluu.org/blog/" title="Gluu Blog">Blog</a></li>
              <li><a href="https://support.gluu.org/" title="Support Center">Support</a></li>
              <li><a href="http://news.gluu.org" title="Industry News">News</a></li>
              <li><a href="http://gluu.org/docs" title="Gluu Server Documentation">Documentation</a></li>
            </ul>
            <ul class="social-links">
              <li><a class="twitter_ic" href="https://twitter.com/GluuFederation">&nbsp;</a></li>
              <li><a class="utube_ic" href="https://www.youtube.com/user/GluuOrg">&nbsp;</a></li>
              <li><a class="in_ic" href="http://www.linkedin.com/company/gluu-inc.">&nbsp;</a></li>
              <li><a class="slideshare_ic" href="http://www.slideshare.net/gluu">&nbsp;</a></li>
            </ul>
          </div>
        </b-col>
        <b-col md="7">
          <b-row>
            <supp-footer-feed feedType="Press Releases"></supp-footer-feed>
            <supp-footer-feed feedType="Last Tweets"></supp-footer-feed>
          </b-row>
        </b-col>
        <b-col md="3">
          <h4>Questions?</h4>
          <div>
            <a href="http://gluu.youcanbook.me" class="gray-btn md">
              <span>Schedule a Demo</span>
              <i class="gluu_ic general-chevron"></i>
            </a>
          </div>
        </b-col>
      </b-row>
      <b-row>
        <b-col sm="12">
          <hr class="bottom-footer-line">
        </b-col>
      </b-row>
      <b-row>
        <b-col sm="12">
          <ul class="list-inline copyright-list">
            <li class="list-inline-item">@ 2009-2018 Gluu, Inc.</li>
            <li class="list-inline-item"><a href="http://www.gluu.org/terms">Terms</a></li>
            <li class="list-inline-item"><a href="http://www.gluu.org/privacy-policy">Privacy Policy</a></li>
          </ul>
        </b-col>
      </b-row>
    </b-container>
  </footer>
</template>

<script>
import SuppFooterFeed from '@/components/SuppFooterFeed'

export default {
  name: 'SuppFooter',
  components: {
    SuppFooterFeed
  }
}
</script>

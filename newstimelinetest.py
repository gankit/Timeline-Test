from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

template = """<html xmlns="http://www.w3.org/1999/xhtml" dir="ltr" lang="en-US"
     xmlns:fb="https://www.facebook.com/2008/fbml"> 

  <head prefix="og: http://ogp.me/ns# pulse_test: 
            http://ogp.me/ns/apps/pulse_test#"> 
    <meta property="fb:app_id" content="264376393584773" /> 
    <meta property="og:type" content="pulse_test:%s" /> 
%s
</head>
</html> """

meta_property = """    <meta property="og:%s" content="%s" /> \n"""

def getMetaTag(prop, content):
    return meta_property % (prop, content)

class GetSource(webapp.RequestHandler):
  def get(self):
      title = self.request.get('title')
      url = self.request.get('url')
      image_url = self.request.get('image')
      description = self.request.get('description')      

      meta_props = getMetaTag('url', self.request.url)

      if title:
          meta_props += getMetaTag('title', title)

      if url:
          meta_props += getMetaTag('source_url', url)
          
      if image_url:
          meta_props += getMetaTag('image', image_url)

      if description:
          meta_props += getMetaTag('description', description)

      html = template % ("source", meta_props) 
      self.response.out.write(html)


class GetStory(webapp.RequestHandler):
  def get(self):
      title = self.request.get('title')
      url = self.request.get('url')
      image_url = self.request.get('image')
      description = self.request.get('description')      
      source_url = self.request.get('source_url')
      source_name = self.request.get('source_name')
      source_desc = self.request.get('source_description')
      source_image = self.request.get('source_image')

      meta_props = getMetaTag('url', self.request.url)

      if source_name and source_url:
          host_url = self.request.host_url
          source_object_url = host_url + "/source"
          source_object_url = "%s?title=%s&url=%s" % (source_object_url,
                                                             source_name,
                                                             source_url)      
          if source_desc:
              source_object_url += "&description=" + source_desc
          if source_image:
              source_object_url += "&image=" + source_image

          meta_props += getMetaTag('source', source_object_url)

      if title:
          meta_props += getMetaTag('title', title)

      if url:
          meta_props += getMetaTag('story_url', url)
          
      if image_url:
          meta_props += getMetaTag('image', image_url)

      if description:
          meta_props += getMetaTag('description', description)

      html = template % ("story", meta_props) 
      self.response.out.write(html)

application = webapp.WSGIApplication(
    [
     ('/source', GetSource),
     ('/story', GetStory)],
    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

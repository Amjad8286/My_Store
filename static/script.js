jQuery(function($) {
  var targets = ['Facebook', 'LinkedIn', 'Twitter', 'Google+'];
  $('.popup').BEShare({
    'class': 'popup-share',
    //'targets': 'Facebook,Twitter|Print,Email',
    'targets': targets,
    'via': 'BrandExtract'
  });

  $('.inline-share').BEShare({
    'type': 'inline',
    'targets': targets.concat(['|', 'Print', 'Email']),
    'via': 'BrandExtract',
    'onShare': function(targetName) {
      ga('send', 'event', 'Social', 'Click', 'Share', targetName);
    }
  });
});
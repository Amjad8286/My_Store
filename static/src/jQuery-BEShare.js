/* jshint browser:true,jquery:true */

;(function($, window, document, undefined) {
  "use strict";
  /*jshint scripturl:true, -W084*/

  var $window = $(window), $document = $(document);

  var TARGETS = {
    'Facebook': 'https://www.facebook.com/sharer/sharer.php?u={$url}&t={$title}',
    'Twitter': 'https://twitter.com/intent/tweet?text={$title}&url={$url}&via={$via}',
    'LinkedIn': 'https://www.linkedin.com/shareArticle?mini=true&url={$url}&title={$title}',
    'Google+': 'https://plus.google.com/share?url={$url}',
    'Print': 'javascript:window.print()',
    'Email': 'mailto:?subject={$title}&body={$url}',
    'SMS': 'sms://?&body={$title}%20-%20{$url}'
  };

  var PLUGIN_NAME = 'BEShare';
  var defaults = {
    'type': 'popup',
    'targets': ['Facebook', 'Twitter'],
    'class': PLUGIN_NAME,
    'prefix': 'icon-',
    'suffix': '',
    'aria-prefix': 'Share on ',
    'width': '626',
    'height': '436',
    'message': document.title,
    'via': '',
    'onShare': null,
    'altLink': null,
    'removeHash': false
  };

  // Mini template engine.
  function template(tpl, data) {
    var re = /\{\$([^}]+)?\}/g, match;
    while(match = re.exec(tpl)) {
      tpl = tpl.replace(match[0], data[match[1]]);
    }
    return tpl;
  }

  function move($element, offset) {
    if (!offset) {
      offset = {
        'top': '-9999px',
        'left': '-9999px'
      };
    }
    $element.css(offset);
  }

  function Plugin(element, options) {
    this.element = $(element);
    this.options = $.extend({}, defaults, options);

    this._name = PLUGIN_NAME;
    this.init();
  }

  Plugin.prototype.init = function() {
    var options = this.options, $container;
    if (options.type === "inline") {
      $container = this.element;
    } else {
      $container = $('<div/>');
      $container.appendTo(document.body);
      $container.css({
        'position': 'absolute'
      });
      move($container);
    }
    this.container = $container;
    $container.addClass(options['class']);

    var targets = options.targets;
    if ($.type(targets) === 'string') {
      // @TODO: Parse string 'ServiceA,ServiceB|ServiceC,ServiceD'
    }

    var i, total = targets.length;
    for (i = 0; i < total; i++) {
      this.add(targets[i]);
    }

    if (options.type === 'popup') {
      this.element.on('click.'+PLUGIN_NAME, function(event) {
        // Stop the event from bubbling up to the below handler.
        event.stopPropagation();

        var position = $(this).offset();

        move($container, position);
        $container.addClass('active');
        return false;
      });

      // Clicking anywhere outside will close the popup.
      $document.on('click.'+PLUGIN_NAME, function(event) {
        if(!$(event.target).closest('.'+options['class']).length) {
          if ($container.hasClass('active')) {
            $container.removeClass('active');
            move($container);
          }
        }
      });
    }
  };

  Plugin.prototype.add = function(targetName) {
    var options = this.options;
    var target = TARGETS[targetName];
    if (!target) {
      // Any string not of a target is output as is.
      this.container.append(targetName);
      return this;
    }

    var builtUrl = this.element.attr('href') || document.location.href;

    if(options.removeHash) {
      builtUrl = builtUrl.split("#")[0]
    }

    if(options.altLink) {
      builtUrl = builtUrl + "/" + (this.element.attr('rel') || '');
    }

    var url = template(target, {
      url: encodeURIComponent(builtUrl),
      title: encodeURIComponent(options.message),
      via: encodeURIComponent(options.via)
    });

    var $link = $('<a href="' + url + '"><span>' + targetName + '</span></a>');

    switch (targetName) {
      case 'Print':
        $link.attr('title', 'Print this page');
        break;
      case 'Email':
        $link.attr('title', 'Share this page via Email');
        break;
      default:
        $link.attr('title', 'Share this page on ' + targetName);
        break;
    }

    if (url.indexOf('http') === 0) {
      // External links
      $link.attr('target', '_blank');
      $link.on('click.'+PLUGIN_NAME, function() {
        window.open(url, PLUGIN_NAME, 'toolbar=0,status=0,width='+options.width+',height='+options.height);

        if (options.onShare) {
          options.onShare(targetName);
        }
        return false;
      });
    }

    $link.addClass(options.prefix + targetName.toLowerCase().replace('+','plus') + options.suffix);
    $link.attr('aria-label', options["aria-prefix"] + targetName.toLowerCase().replace('+','plus'));
    $link.appendTo(this.container);
    return this;
  };

  $.fn[PLUGIN_NAME] = function(options) {
    return this.each(function() {
      if (!$.data(this, 'plugin_' + PLUGIN_NAME)) {
        $.data(this, 'plugin_' + PLUGIN_NAME,
        new Plugin( this, options ));
      }
    });
  };
})(jQuery, window, document);

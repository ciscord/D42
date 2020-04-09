/**
 * website
 * (c) Device42 <dave.amato@device42.com>
 */

var browserSync = require('browser-sync');
var config = require('./.taskconfig');
var gulp = require('gulp');
var path = require('path');
var sequence = require('run-sequence');
var spawn = require('child_process').spawn;
var $util = require('gulp-util');

gulp.task('serve', function() {
  if (config.env.watch && !config.debug) {
    $util.log($util.colors.yellow('Watch is not supported in production. Please specify ') + '--debug' + $util.colors.yellow(' instead.'));
    return;
  }

  if (config.debug) {
    spawn('python', [path.join(config.paths.src, 'manage.py'), 'runserver', config.serve.browserSync.proxy, '--insecure'], { stdio: 'inherit' });
  }
  else {
    spawn('python', [path.join(config.paths.build, 'manage.py'), 'runserver', config.serve.browserSync.proxy, '--insecure', '--settings=project.settings.prod'], { stdio: 'inherit' });
  }

  browserSync(config.serve.browserSync);

  if (config.env.watch) {
    var entries = config.watch.entries;
    for (var i = 0; i < entries.length; i++) {
      var entry = entries[i];
      gulp.watch(entry.files, entry.tasks.concat(browserSync.reload));
    }
  }
});

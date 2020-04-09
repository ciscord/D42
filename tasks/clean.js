/**
 * website
 * (c) Device42 <dave.amato@device42.com>
 */

var config = require('./.taskconfig');
var del = require('del');
var gulp = require('gulp');

/**
 * Cleans /.tmp and /build directories.
 */
gulp.task('clean', function(callback) {
  del(config.clean.entry).then(function(paths) {
    callback();
  });
});

gulp.task('clean_tmp', function(callback) {
    del(config.clean.tmp).then(function(paths) {
        callback();
    });
});

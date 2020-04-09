/**
 * website
 * (c) Device42 <dave.amato@device42.com>
 */

var config = require('./.taskconfig');
var gulp = require('gulp');
var path = require('path');
var spawn = require('child_process').spawn;
var prompt = require('gulp-prompt');
var imagemin = require('gulp-imagemin'),
	pngquant = require('imagemin-pngquant');
/**
 * Runs Django shell.
 */
gulp.task('shell', function() {
  spawn('python', [path.join(config.paths.src, 'manage.py'), 'shell'], {
    stdio: 'inherit'
  });
});

/**
 * Runs Django migration.
 */
gulp.task('migrate', function() {
  spawn('python', [path.join(config.paths.src, 'manage.py'), 'migrate', '--run-syncdb'], {
    stdio: 'inherit'
  });
});

/**
 * Image optimization.
 */
gulp.task('optimize', function() {
	return gulp.src(config.images.entry)
				.pipe(imagemin())
				.pipe(gulp.dest(config.paths.optimized));
});






/**
 * website
 * (c) Device42 <dave.amato@device42.com>
 */

var autoprefixer = require('autoprefixer');
var babelify = require('babelify');
var browserify = require('browserify');
var browserSync = require('browser-sync');
var buffer = require('vinyl-buffer');
var config = require('./.taskconfig');
var cssnano = require('cssnano');
var del = require('del');
var gulp = require('gulp');
var path = require('path');
var source = require('vinyl-source-stream');
var spawn = require('child_process').spawn;
var through2 = require('through2');
var watchify = require('watchify');
var $if = require('gulp-if');
var $htmlmin = require('gulp-htmlmin');
var $postcss = require('gulp-postcss');
var $sass = require('gulp-sass');
var $size = require('gulp-size');
var $sourcemaps = require('gulp-sourcemaps');
var $uglify = require('gulp-uglify');
var $util = require('gulp-util');
var changed = require('gulp-changed');
var notify = require('gulp-notify');
var spritesmith = require('gulp.spritesmith');
var merge = require('merge-stream');

var handleError = function(task) {
  return function(err) {
    notify.onError({
      message: task + ' has failed: ' + err,
      sound: false
    })(err);
    $util.log($util.colors.bgRed(task + ' error:'), $util.colors.red(err));
  };
};
var handleDebug = function(task) {
  return function(msg) {
    $util.log($util.colors.bgBrightBlue('[DEBUG] ' + task + ': ' + msg));
  }
}

gulp.task('images', function () {
  return gulp.src(config.images.entry)
    .pipe($size({title: '[images]', gzip: true}))
    .pipe(gulp.dest(config.images.output));
});

gulp.task('videos', function () {
  return gulp.src(config.videos.entry)
    .pipe($size({title: '[videos]', gzip: true}))
    .pipe(gulp.dest(config.videos.output));
});

gulp.task('fonts', function() {
  return gulp.src(config.fonts.entry)
    .pipe($size({ title: '[fonts]', gzip: true }))
    .pipe(gulp.dest(config.fonts.output));
});

gulp.task('styles', function () {
  var postcssPlugins = [autoprefixer(config.styles.autoprefixer)];
  if (config.debug) postcssPlugins.push(cssnano());


  return gulp.src(config.styles.entry)
    .pipe($if(config.debug, $sourcemaps.init()))
    .pipe($sass({
      sourceComments: config.debug,
      outputStyle: config.debug ? 'nested' : 'compressed'
    }))
    .on('error', handleError('SASS'))
    .pipe($if(config.debug, $sourcemaps.write({
      'includeContent': false
    })))
    .pipe($if(config.debug, $sourcemaps.init({
      'loadMaps': true
    })))
    .pipe($postcss([autoprefixer(config.styles.autoprefixer)]))
    .pipe($sourcemaps.write({
      'includeContent': true
    }))
    .pipe($size({ title: '[styles]', gzip: true }))
    .pipe(gulp.dest(config.styles.output));
});

gulp.task('javascript', function () {
  var isWatching = false;

  return gulp.src(config.scripts.entry)
    .pipe(through2.obj(function (file, enc, next) {
      var opts = {
        entries: [file.path],
        debug: config.debug,
        transform: [babelify],
        cache: {}
      };
      var bundler = (config.env.watch) ? watchify(browserify(opts)) : browserify(opts);
      var output = file.path.replace(file.base, '');

      if (config.env.watch) {
        bundler.on('time', function (time) {
          $util.log($util.colors.blue('[browserify]'), output, $util.colors.magenta('in ' + time + 'ms'));
        });
        bundler.on('update', function () {
          bundle(bundler, output);
        });
      }

      bundle(bundler, output, next).on('end', function () {
        next(null, file);
      });
    }));

  function bundle(bundler, output, next) {
    return bundler.bundle()
      .on('error', function (err) {
        $util.log($util.colors.blue('[browserify]'), $util.colors.red('Error: ' + err.message));
        if (next) next(); else this.emit('end');
      })
      .on('end', function () {
        if (isWatching) browserSync.reload();
        isWatching = config.env.watch;
      })
      .pipe(source(output))
      .pipe(buffer())
      .pipe($if(config.debug, $sourcemaps.init({loadMaps: true})))
      .pipe($if(!config.debug, $uglify()))
      .pipe($if(config.debug, $sourcemaps.write('./')))
      .pipe(gulp.dest(config.scripts.output));
  }

});

gulp.task('core', function () {
  return gulp.src(config.core.entry, {dot: true})
    .pipe(gulp.dest(config.core.output));
});

gulp.task('templates', function () {
  return gulp.src(config.templates.entry)
    .pipe($if(!config.debug, $htmlmin(config.templates.htmlmin)))
    .pipe($size({
      title: '[templates]',
      gzip: true
    }))
    .pipe(gulp.dest(config.templates.output));
});

gulp.task('browserify', function() {
  var bundler = browserify(config.scripts.entry, {
    debug: config.debug,
    cache: {},
    transform: [babelify]
  });
  var build = config.env.build ? 'build' : false;
  if (config.env.watch) {
    bundler = watchify(bundler);
  }
  var rebundle = function() {
    return bundler.bundle()
      .on('error', handleError('Browserify'))
      .pipe(source('build.js'))
      .pipe($if(!config.debug, buffer()))
      .pipe($if(!config.debug, $uglify()))
      .pipe(gulp.dest(config.scripts.output));
  };
  bundler.on('update', rebundle);
  return rebundle();
});

gulp.task('sass', function() {
  return gulp.src(config.styles.entry)
    .pipe($if(config.debug, $sourcemaps.init()))
    .pipe($sass({
      sourceComments: config.debug,
      outputStyle: config.debug ? 'nested' : 'compressed'
    }))
    .on('error', handleError('SASS'))
});

gulp.task('static', ['images', 'videos', 'fonts', 'styles', 'browserify']);

gulp.task('build', ['core', 'templates', 'static'], function (done) {
    var fs = require('fs');

    var walk = function (dir, done) {
        var results = [];
        fs.readdir(dir, function (err, list) {
            if (err) return done(err);
            var i = 0;
            (function next() {
                var file = list[i++];
                if (!file) return done(null, results);
                file = path.join(dir, file);
                fs.stat(file, function (err, stat) {
                    if (stat && stat.isDirectory()) {
                        results.push({f: file, d: true});
                        walk(file, function (err, res) {
                            results = results.concat(res);
                            next();
                        });
                    } else {
                        results.push({f: file, d: false});
                        next();
                    }
                });
            })();
        });
    };
    walk(path.join(config.paths.tmp, 'static'), function (err, files) {
        files.forEach(function (f, i) {
            spawn('/usr/bin/cmp', ['--silent', f.f, f.f.replace(config.paths.tmp, config.paths.build)]).on('exit', function (code) {
                if ((code == 0) || (f.d)) {
                    if (fs.existsSync(f.f.replace(config.paths.tmp, config.paths.build))) {
                        var originalFileStats = fs.statSync(f.f.replace(config.paths.tmp, config.paths.build));
                        var atime = new Date(originalFileStats.atime);
                        var mtime = new Date(originalFileStats.mtime);
                        fs.utimesSync(f.f, atime.getTime() / 1000, mtime.getTime() / 1000);
                    }
                }
            });
        });

        if (!config.debug && !config.env.skipcollect) {
            $util.log($util.colors.blue('[STARTING]'), $util.colors.red('Deployment of static files to AWS S3'));
            spawn('python', [path.join(config.paths.src, 'manage.py'), 'collectstatic', '--noinput'], {
                stdio: 'inherit'
            }).on('exit', function (code) {
                if (code === 0) {
                    $util.log($util.colors.green('[SUCCESS]'), $util.colors.green('Build completed'))
                    spawn('/home/shivji/d42/rsync.sh', [], {
                        stdio: 'inherit'
                    }).on('exit', function(code) {
                        if (code === 0) {
                            return;
                        }
                    }).on('error', function(code) {
                      $util.log($util.colors.red('[FAILED]'), $util.colors.red('Error trying to rsync static files!'))
                    })
                }
            });
        } else {
          $util.log($util.colors.blue('[SKIPPED]'), $util.colors.yellow('Skipped static files rsync'));
          done();
          $util.log($util.colors.green('[SUCCESS]'), $util.colors.green('Built completed successfully'));
        }
    });
});

gulp.task('sprites', ['sprites:logos', 'sprites:integrations', 'sprites:home'])

gulp.task('sprites:integrations', function() {
  var spriteData = gulp.src(config.sprites.folders.integrations)
    .pipe(spritesmith({
      imgName: 'sprite-integrations.png',
      cssName: '_sprite-integrations.scss',
      cssTemplate: config.sprites.template,
      padding: 2,
    }));

  spriteData.img.pipe(gulp.dest(config.sprites.imgOutput));
  spriteData.css.pipe(gulp.dest(config.sprites.cssOutput));
})

gulp.task('sprites:logos', function(){
  var spriteData = gulp.src(config.sprites.folders.logos)
    .pipe(spritesmith({
      imgName: 'sprite-logos.png',
      cssName: '_sprite-logos.scss',
      cssTemplate: config.sprites.template,
      padding: 2,
      // algorithm: 'top-down'
    }));
  spriteData.img.pipe(gulp.dest(config.sprites.imgOutput));
  spriteData.css.pipe(gulp.dest(config.sprites.cssOutput));
});
gulp.task('sprites:home', function(){
  var spriteData = gulp.src(config.sprites.folders.home)
    .pipe(spritesmith({
      imgName: 'sprite-home.png',
      cssName: '_sprite-home.scss',
      cssTemplate: config.sprites.template,
      padding: 2,
      // algorithm: 'top-down'
    }));
  spriteData.img.pipe(gulp.dest(config.sprites.imgOutput));
  spriteData.css.pipe(gulp.dest(config.sprites.cssOutput));
});

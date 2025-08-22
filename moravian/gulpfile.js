const gulp = require('gulp');
const cleanCSS = require('gulp-clean-css');
const concat = require('gulp-concat');

const paths = {
  css: [
    'moravian/static/css/gridh.css',
    'moravian/static/css/custom.css',
    'moravian/static/css/mobile.css',
  ],
  output: 'moravian/static/css/'
};

// Minify css to one file. Run "npx gulp minify".
gulp.task('minify', function () {
  return gulp.src(paths.css)
    .pipe(concat('minified.css'))
    .pipe(cleanCSS({ compatibility: 'ie8' }))
    .pipe(gulp.dest(paths.output));
});

// Rebuild automatically when changed. Run "npx gulp watch".
gulp.task('watch', function () {
    gulp.watch(paths.css, gulp.series('minify'));
  });
  
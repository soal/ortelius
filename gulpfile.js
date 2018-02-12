var gulp = require("gulp"),
    exec = require("child_process").exec,
    fork = require("child_process").fork,
    spawn = require("child_process").spawn;
gulp.task("devServer", () => {
  var child = spawn("sh", ["devServer.sh"]);
  // spawn("killall", ["hug"]);
  // var child = spawn("hug", ["-f", "ortelius/app.py", "-p 8000"]);
  // var child = exec("python ./manage.py run");
  child.stdout.on('data', function(chunk) {
      text = chunk.toString('utf8');
      console.log("Info:");
      console.log(text);
      console.log("End Info");
  });
  child.stderr.on('data', function(chunk) {
      text = chunk.toString('utf8');
      console.log("Error:")
      console.log(text);
      console.log("End Error")
  });
  child.on('error', function(err){
      console.log(err);
  })
  return child
});

gulp.task("watch", ["devServer"], () => {
  gulp.watch("./**/*.py", ["devServer"]);
});


gulp.task("default", ["watch"]);

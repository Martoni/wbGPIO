val majorChiselVersion = "6"
val minorChiselVersion = "2"
val chiselVersion = majorChiselVersion + "." + minorChiselVersion + ".0"

scalaVersion     := "2.13.12"
version          := majorChiselVersion + "." + minorChiselVersion + ".0"
organization     := "org.armadeus"

lazy val root = (project in file("."))
  .settings(
    name := "wbGpio",
    libraryDependencies ++= Seq(
      "org.chipsalliance" %% "chisel" % chiselVersion,
      "org.scalatest" %% "scalatest" % "3.2.16" % "test",
      "org.armadeus" %% "wbplumbing" % "6.2.5"
    ),
    scalacOptions ++= Seq(
      "-language:reflectiveCalls",
      "-deprecation",
      "-feature",
      "-Xcheckinit",
      "-Ymacro-annotations",
    ),
    addCompilerPlugin("org.chipsalliance" % "chisel-plugin" % chiselVersion cross CrossVersion.full),
  ).dependsOn(wbplumbing)

lazy val wbplumbing = RootProject(uri("https://github.com/Martoni/WbPlumbing.git"))

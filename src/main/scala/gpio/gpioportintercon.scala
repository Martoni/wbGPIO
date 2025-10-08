package gpio

import chisel3._
import chisel3.util._

import scala.util.control.Breaks._

/*
 * This module will map portVec to port according to the gpioMaps.
 * Example: If gpioMaps is Seq((0,9), (10, 19)), this module will map
 * portVec(0) to port(9, 0) and portVec(1) to port(19, 10).
 */
class GpioPortIntercon(gpioMaps: Seq[Range], portsize: Int) extends Module {

  val io = IO(new Bundle {
    val portVec = MixedVec(for (r <- gpioMaps) yield  new GpioPort(r.length))
    val port = Flipped(new GpioPort(portsize))
  })


  // Parameters checks
  for ((r1, pIdx) <- gpioMaps.zipWithIndex) {
    for (r2 <- gpioMaps) {
      breakable {
        if (r1 == r2) {
          break()
        }

        assert(!(r1.contains(r2.start) || r1.contains(r2.end)), "GPIO range overlap")
      }
    }

    assert((r1.start < portsize) && (r1.end < portsize), "source port bounds is outside destination port")
    assert(r1.length == io.portVec(pIdx).portsize, "GPIO range and portsize differ")
  }

  val inportV = Wire(Vec(portsize, Bool()))

  inportV := DontCare
  for ((range, pIdx) <- gpioMaps.zipWithIndex) {
    for (l <- range) {
      inportV(l) := io.portVec(pIdx).inport(l - range.start)
    }

    io.portVec(pIdx).outport := io.port.outport(range.end, range.start)
    io.portVec(pIdx).enport := io.port.enport(range.end, range.start)
  }

  io.port.inport <> inportV.asUInt
}

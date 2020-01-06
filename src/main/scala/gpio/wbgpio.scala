package gpio 

import chisel3._
import chisel3.util._
import chisel3.experimental._
import chisel3.Driver

import wbplumbing.WbSlave

class WbGpio(val portsize: Int = 16) {
  val io = IO(new Bundle{
     val wbs = new WbSlave(16, 2, "mdio")

     /* tristate buffer port IO */
     val outport = Output(UInt(portsize.W))
     val enport = Output(UInt(portsize.W))
     val inport = Input(UInt(portsize.W))
  })

  val version = 1

  /* registers */
  val STATUSADDR := 0.U // R
  val DIRADDR    := 1.U // R/W
  val READADDR   := 2.U // R
  val WRITEADDR  := 3.U // R/W

  /* status (R) : 0x0
   *  | X .. 8|   7..0  |
   *  |-------|---------|
   *  |  void | version |
   *  |-------|---------|
   */
  val statusReg = RegInit(version.U(portsize.W))

  /* direction (R/W) : 0x1
   * |    X..0   |
   * |-----------|
   * | direction |
   * |-----------|
   */
  val dirReg = RegInit(0.U(portsize.W))
  io.enport := dirReg

  /* read (R) : 0x2
   * |   X..0  |
   * |---------|
   * | readreg |
   * |---------|
   */
  //io.inport

  /* write (R/W) : 0x3
   * |   X..0   |
   * |----------|
   * | writereg |
   * |----------|
   */
  val writeReg = RegInit(0.U(portsize.W))
  io.outport:= writeReg

  // Wishbone state machine
  //     00       01        10
  val swbinit::swbread::swbwrite::Nil = Enum(3)
  val wbSm = RegInit(swbinit)
  val ackReg = RegInit(false.B)
  val wbReadReg = RegInit(0.U(dataSize.W))

  ackReg := false.B
  switch(wbSm){
    is(swbinit){
     when(io.wbs.stb_i & io.wbs.cyc_i & !ackReg){
        when(io.wbs.we_i){ // writing
          switch(io.wbs.adr_i) {
            is(DIRADDR){
              dirReg := io.wbs.dat_i
            }
            is(WRITEADDR){
              writeReg := io.wbs.dat_i
            }
          }
          wbSm := swbwrite
        }.otherwise { // reading
          switch(io.wbs.adr_i){
            is(STATUSADDR){
              wbReadReg := statusReg
            }
            is(DIRADDR){
              wbReadReg := dirReg
            }
            is(READADDR){
              wbReadReg := io.inport
            }
            is(WRITEADDR){
              wbReadReg := writeReg
            }
          }
          wbSm := swbread
        }
      }
    }
    is(swbread){
      wbSm := swbinit
    }
    is(swbwrite){
      wbSm := swbinit
    }
  }

  ackReg := (wbSm === swbread) || (wbSm === swbwrite)

  io.wbs.dat_o := wbReadReg
  io.wbs.ack_o := ackReg

}

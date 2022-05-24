const myfunction = (output) =>{
    Swal.fire({
        // timer: Swal.isTimerRunning(),
        title: output,
        titleText: output,
        showClass: {
          popup: 'animate__animated animate__fadeInDown'
        },
        hideClass: {
          popup: 'animate__animated animate__fadeOutUp'
        }

      })
    }
 function handelclick(e) { 
        e.preventDefault()
    }

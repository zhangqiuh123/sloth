    $(document).ready(function() {
           $(".tree label").click(function(){
               var isChecked = $(this).next("input[type='checkbox']").is(':checked');
               if(isChecked){
                   $(this).css(
                       "background-image","url(../images/cp-detail-arrow-b.png)"
                   );
               }else{
                   $(this).css(
                       "background-image","url(../images/cp-detail-arrow-t.png)"
                   );
               }
           });
            
       });
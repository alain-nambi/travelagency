(function(d){
    var notif_number = document.getElementById('notif_number');
    var badge = document.getElementById('badge');
    
    var int = window.setInterval(updateBadge, 2000); //Update the badge every 5 seconds
    var badgeNum;    
    function updateBadge(){//To rerun the animation the element must be re-added back to the DOM
          var badgeChild = badge.children[0];
              if(badgeChild.className==='badge-num')
                  badge.removeChild(badge.children[0]);
          
          badgeNum = document.createElement('div'); 
        badgeNum.setAttribute('class','badge-num');
             badgeNum.innerHTML = notif_number;
          var insertedElement = badge.insertBefore(badgeNum,badge.firstChild); 
        console.log(badge.children[0]);
    }
  })(document);
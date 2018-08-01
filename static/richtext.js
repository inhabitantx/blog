// ################## quillJS ################

//initialize quilljs

var options = {
  debug: 'info',
  placeholder: 'Compose an epic...',
  readOnly: true,
  theme: 'snow'
};

var quill = new Quill('#editor', options );

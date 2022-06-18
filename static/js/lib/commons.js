define(['require','filters','ajax_api', 'element_utils', 'editor/editor', 
    'editor/plugins/header.min','editor/plugins/list.min', 'editor/plugins/link.min',
    'editor/plugins/checklist.min', 'editor/plugins/quote.min', 'editor/plugins/table.min',
    'editor/plugins/inline-image','editor/plugins/editor-emoji.min'
    ], function(require,Filter,ajax_api, element_utils,EditorJS) {
    'use strict';

    const Header = require('editor/plugins/header.min');
    const List = require('editor/plugins/list.min');
    const Link = require('editor/plugins/link.min');
    const Checklist = require('editor/plugins/checklist.min');
    const Quote = require('editor/plugins/quote.min');
    const Emoji = require('editor/plugins/editor-emoji.min');
    const Table = require('editor/plugins/table.min');
    const InlineImage = require('editor/plugins/inline-image');
    
    const SAVE_DRAFT_INTERVAL = 10000; // 10s
    const EDITOR_CHANGE_TIMEOUT = 1000; // 1s
    const COMMENT_FETCH_INTERVAL = 15000; // 30s
    const POST_STATUS_PUBLISH = 1
    const CAROUSEL_INTERVAL = 5000;
    const MIN_LEN_WARNING = 20;
    const MAX_COMMENT_TEXT_LEN = 256;
    const LOGIN_REQUIRED_KEY = "login_required";
    let isDirty = false;
    let AUTO_SAVE_TIMER;
    let fileUpload;
    let postManager;
    let messages;
    let notification_wrapper;
    let fadeDelay = 10000; // 10s
    let filter_form;
    let editor;
    let post_content;
    let json_input;
    let headers = [null, "h1","h2", "h3", "h4", "h5", "h6"];
    let LIST_TYPE_MAPPING = {
        ordered: 'ol',
        unordered:'ul',
        checklist: 'ul'
    };

    let BLOCK_MAPPING = {
        'header': render_header,
        'paragraph': render_paragraph,
        'table': render_table,
        'list': render_list,
        'linkTool': render_linkTool,
        'checklist': render_checklist,
        'quote': render_quote,
        'image': render_inlineImage,
        'emoji': render_emoji
    };
    function render_emoji(emoji){
        console.log(emoji);
        return emoji.data.text;
    }

    function render_header(header){
        let node = element_utils.create_element_api({
            element:headers[header.data.level],
            options : {
                id:header.id,
                innerHTML: header.data.text
            }
        });
        return node;
    }

    function render_linkTool(linkTool){
        let node = element_utils.create_element_api({
            element: "a",
            options : {
                id:linkTool.id,
                cls:'mat-button mat-button-text',
                href : linkTool.data.link,
                innerText: linkTool.data.link
            }
        });
        return node;
    }

    function render_inlineImage(inlineImage){
        let node = element_utils.create_element_api({
            element: "img",
            options : {
                id:inlineImage.id,
                src: inlineImage.data.url,
                title: inlineImage.data.caption,
                cls:'img-responsive',
            }
        });
        return node;
    }

    function render_paragraph(paragraph){
        let node = element_utils.create_element_api({
            element: "p",
            options : {
                id:paragraph.id,
                innerHTML : paragraph.data.text
            }
        });
        return node;
    }

    function render_table(table){
        let items = [];
        let startIndex = 0;
        let content;

        if(table.data.withHeadings){
            
            let ths = [];
            table.data.content[startIndex].forEach((h)=>{
                ths.push(element_utils.create_element_api({
                    element:'th',
                    options:{
                        innerHTML:h
                    }
                }));
            });
            let tr = element_utils.create_element_api({
                element: 'tr',
                options:{
                    children: ths
                }
            });
            items.push(element_utils.create_element_api({
                element: 'thead',
                options:{
                    children: [tr]
                }
            }));

            startIndex = 1;
            content = table.data.content.slice(startIndex);
        }else{
            content = table.data.content;
        }

        let trs = [];
        content.forEach((item)=>{
            let tds = [];
            item.forEach((value) => tds.push(element_utils.create_element_api({
                element: "td",
                options : {
                    innerText : value
                }
            })));
            trs.push(element_utils.create_element_api({
                element: "tr",
                options : {
                    children : tds
                }
            }));
        });
        items.push(element_utils.create_element_api({
            element: "tbody",
            options : {
                children: trs
            }
        }));
        let node = element_utils.create_element_api({
            element: table.type,
            options : {
                id:table.id,
                children : items
            }
        });
        return node;
    }

    function render_list(list){
        let items = []
        list.data.items.forEach((item)=>{
            items.push(element_utils.create_element_api({
                element: "li",
                options : {
                    innerHTML : item
                }
            })
            );
        });
        let node = element_utils.create_element_api({
            element: LIST_TYPE_MAPPING[list.data.style],
            options : {
                id:list.id,
                children : items
            }
        });
        return node;
    }

    function render_checklist(checklist){
        let items = []
        checklist.data.items.forEach((item)=>{
            let input = element_utils.create_element_api({
                element : "input",
                options : {
                    'type': 'checkbox',
                    'checked': item.checked
                }
            });
            let span = element_utils.create_element_api({
                element: "span",
                options : {
                    innerHTML : item.text
                }
            });
            let div = element_utils.create_element_api({
                element: "div",
                options : {
                    children : [input, span]
                }
            });
            items.push(element_utils.create_element_api({
                element: "li",
                options : {
                    children : [div]
                }
            })
            );
        });
        let node = element_utils.create_element_api({
            element: LIST_TYPE_MAPPING[checklist.type],
            options : {
                id:checklist.id,
                children : items
            }
        });
        return node;
    }

    function render_quote(quote){
        let span = element_utils.create_element_api({
            element: "span",
            options : {
                innerHTML : quote.data.text
            }
        });
        let cite = element_utils.create_element_api({
            element: "cite",
            options : {
                innerHTML : quote.data.caption
            }
        });
        let node = element_utils.create_element_api({
            element: "blockquote",
            options : {
                id:quote.id,
                innerHTML : quote.data.text,
                children: [cite]
            }
        });
        return node;
    }

    
    function editor_content_clear(container){
        let editor_content = container || document.querySelector('#editor-content');
        if (editor_content){
            while(editor_content.firstChild){
                editor_content.removeChild(editor_content.firstChild);
            }
        }
    }

    function render_content(blocks){
        let elements = [];
        blocks.forEach((block)=>{
            elements.push(BLOCK_MAPPING[block.type](block));
        });
        return elements;
    }

    function on_editor_save(saved_data){
        post_content = saved_data;
    }

    function on_editor_change(api, event){
        api.saver.save().then(on_editor_save).catch((error)=>{
            console.log("Error on saving editor content after changes : ", error);
        });
    }

    function fetch_credential(callback){
        let csrfmiddlewaretoken = document.querySelector('input[name="csrfmiddlewaretoken"]');
        if(csrfmiddlewaretoken == null){
            return;
        }
        let url = '/api/fetch-credentials/';
        let formData = new FormData();
        formData.append('csrfmiddlewaretoken', csrfmiddlewaretoken.value);
        let fetch_options = {
            method : 'POST',
            body: formData
        };
        ajax_api.fetch_api(url, fetch_options).then((response)=>{
            editor = callback({appName : response.appName, clientId : response.access_key});
        }, function(reason){
            console.error("Error on fetching unsplash credentials.");
            console.error(reason);
            
        });
    }

    function editor_init(unsplash_conf){
        let editor_tag = document.getElementById('editor');
        let init_data = {};
        if(json_input && json_input.value.length){   
            try {
                init_data = JSON.parse(json_input.value);
                post_content = init_data;
            } catch (error) {
                console.warn("error on parsing json data from description_json value : %s", json_input.value);
                console.error(error);
                init_data = {};
            }
        }
        editor = new EditorJS({
            holder:'editor',
            tools: {
                header : {
                    class : Header,
                    inlineToolbar : true
                },
                image: {
                    class : InlineImage,
                    inlineToolbar : true,
                    config: {
                        embed : {
                            display: true
                        },
                        unsplash : unsplash_conf
                    }
                },
                list: {
                    class: List,
                    inlineToolbar: true
                },
                linkTool: {
                    class: Link,
                    inlineToolbar: true
                },
                emoji: {
                    class:Emoji,
                    inlineToolbar: true
                },
                checklist: {
                    class:Checklist,
                    inlineToolbar:true
                },
                quote: {
                    class:Quote,
                    inlineToolbar:true,
                    shortcut: 'CMD+SHIFT+Q',
                    config: {
                        quotePlaceholder: editor_tag.dataset.quotePlaceholder,
                        captionPlaceholder: editor_tag.dataset.captionPlaceholder,
                    },
                },
                table: {
                    class: Table,
                    inlineToolbar: true,
                    config: {
                      rows: 2,
                      cols: 3,
                    },
                  },
            },
            autofocus: true,
            data: init_data,
            placeholder: editor_tag.dataset.placeholder,
            onReady: function(){
                console.log("Editor is ready" , editor);
            },
            onChange: (api, event) =>{
                if(AUTO_SAVE_TIMER){
                    clearTimeout(AUTO_SAVE_TIMER);
                }
                AUTO_SAVE_TIMER = setTimeout(on_editor_change, EDITOR_CHANGE_TIMEOUT, api, event);
            }
        });
        $(".js-save-btn").on('click', function(event){
            editor.save().then(on_editor_save).catch((error)=>{
                console.log("Error on saving editor content : ", error);
            });
        });
        $(".js-clear-btn").on('click', (event)=>{
            console.log("Clearing editor content not implemented yet ");
        });
        console.log("Editor loaded", editor);

        return editor;
    }


    function create_editor(){
        let editor_tag = document.getElementById('editor');
        json_input = document.getElementById('content');
        if( !editor_tag ){
            return;
        }
        fetch_credential(editor_init);
    }

    function preview_post(){
        let form = document.getElementById('preview-form');
        let preview_title = document.getElementById('preview-title');
        let title = document.getElementById('title');
        let content = document.getElementById('preview-content');
        if(!title || !title.value.length){
            notify({'content' : preview_title.dataset.missingMessage, 'level': 'info'});
            title.classList.add('warning');
            return;
        }
        title.classList.remove('warning');
        preview_title.value = title.value;
        if(!post_content.blocks.length){
            notify({'content' : content.dataset.missingMessage, 'level': 'info'});
            return;
        }
        content.value = JSON.stringify(post_content);
        form.submit();
    }

    function clean_form_before_submit(form){
        let filter_inputs = $('.filter-input', form);
        filter_inputs.each(function(){
            this.disabled = this.value == "";
        });
        $('.no-submit', form).each(function(){
            this.disabled = true;
        });
        let valid_inputs = filter_inputs.filter(function(){
            return this.value != "";
        });
        return valid_inputs.length == 0;
    }
    function notify(message){
        if( typeof notification_wrapper === 'undefined' || typeof messages === 'undefined'){
            console.warn("Notify call for message %s. But There is no messages container", message);
            return;
        }
        let li = $('<li />', {
            "class" : message.level,
        });
        let div = $('<div />', {
            "class" : "notification flex"
        });
        div.append($('<i />', {
            "class" : "fas fa-info-circle icon"
        })).append($('<span />', {
            'text': message.content
        })).appendTo(li);
        li.appendTo(messages);
        notification_wrapper.fadeIn().delay(fadeDelay).fadeOut('slow', function () {
            messages.empty();
        });
    }

    function notify_init(wrapper, message_container){
    
        if(typeof wrapper === 'undefined'){
            console.log("notification_wrapper undefined");
            return;
        }

        if(typeof message_container === 'undefined' || $('li', message_container).length == 0){
            return;
        }

        wrapper.fadeIn().delay(fadeDelay).fadeOut('slow', function () {
            message_container.empty();
            console.log("messages container emptied on init");
        });
    }
    function image_preview(){
        let previewer = document.getElementById('image-previewer');
        if(!previewer){
            return;
        }
        let images = previewer.querySelectorAll('.preview-image');
        if(!images){
            return;
        }
        let max_index = parseInt(previewer.dataset.count);
        let active_image = previewer.querySelector('#active-image');
        let prev_btn = previewer.querySelector('.prev');
        let next_btn = previewer.querySelector('.next');
        let viewer_current_index = previewer.querySelector('.viewer-current-index');
        let current = parseInt(previewer.dataset.current);
        prev_btn.addEventListener('click', function(event){
            event.stopPropagation();
            current--;
            if(current >= 0){
                active_image.src = images[current].src;
                next_btn.classList.remove('disabled');
                previewer.dataset.current = current;
            }else{
                current = 0;
            }
            this.classList.toggle('disabled', current == 0);
            viewer_current_index.innerText = current + 1;
        });
        next_btn.addEventListener('click', function(event){
            event.stopPropagation();
            current++;
            if(current < max_index){
                active_image.src = images[current].src;
                prev_btn.classList.remove('disabled');
                previewer.dataset.current = current;
            }else{
                current = max_index;
            }
            this.classList.toggle('disabled', current >= (max_index - 1));
            viewer_current_index.innerText = current + 1;
        });
    }
    function input_check_max_limit(input){
        //let max_len = parseInt(input.dataset.maxLength);
        let len = input.value.length;
        let target = document.getElementById(input.dataset.target);
        let max_len_reached = len == MAX_COMMENT_TEXT_LEN;
        //$input.toggleClass("warning", max_len_reached);
        if((MAX_COMMENT_TEXT_LEN - len) <= MIN_LEN_WARNING){
            target.innerText = MAX_COMMENT_TEXT_LEN - len;
        }else{
            target.innerText = "";
        }
        target.classList.toggle("danger", (MAX_COMMENT_TEXT_LEN - len) <= 0);
        target.classList.toggle("warning", ((MAX_COMMENT_TEXT_LEN - len) > 0 && (MAX_COMMENT_TEXT_LEN - len) <= MIN_LEN_WARNING));
    }

    function track_action(track_element){
        let csrfmiddlewaretoken = document.querySelector('input[name="csrfmiddlewaretoken"]');
        let url = '/api/track-actions/';
        let action = parseInt(track_element.dataset.action);
        let options = {
            url : url,
            type: 'POST',
            data : {'action': action, 'csrfmiddlewaretoken': csrfmiddlewaretoken.value},
            dataType : 'json',
            async:false,
            cache : false,

        };
        ajax_api.ajax(options).then(function(response){
            
        }, function(reason){
            console.error(reason);
        });
    }
    function clear_uploaded_files(){
        let files_container = document.querySelector('.file-list');
        let input_files = document.querySelector('#files');
        input_files.value = null;
        while(files_container.firstChild){
            files_container.removeChild(files_container.firstChild);
        }
        $('.js-uploaded-files-clear').hide();
    }
    function show_preview(files) {
        let files_container = document.querySelector('.file-list');
        let li;
        let img;
        while(files_container.firstChild){
            files_container.removeChild(files_container.firstChild);
        }
        let f;
        for(let i = 0; i < files.length; i++){
            f = files[i];
            li = document.createElement('li');
            img = document.createElement('img');
            img.src = URL.createObjectURL(f);
            img.height = 60;
            files_container.appendChild(li);
            img.onload = function(){
                URL.revokeObjectURL(img.src);
            };
            li.classList.add('file-entry');
            li.appendChild(img);
            const info = document.createElement('span');
            info.innerHTML = f.name + " : " + f.size + ' bytes';
            li.appendChild(info);
        }
    }

    function onDragInit(){
        var droppedFiles;
        var dragarea = document.querySelector('.drag-area');
        if(!dragarea){
            console.log("no drag-area could be found");
            return;
        }
        var $form = $('#' + dragarea.dataset.form);
        $('.drag-area').on('drag dragstart dragend dragover dragenter drop', function(e){
            e.preventDefault();
            e.stopPropagation();
        }).on('dragover dragenter', function(){
            dragarea.classList.add('on-drag');
        }).on('dragleave dragend drop', function(){
            dragarea.classList.remove('on-drag');
        }).on('drop', function(e){
            droppedFiles = e.originalEvent.dataTransfer.files;
            var input_files = document.querySelector('#files');
            console.log("Droped file : ", droppedFiles);
            console.log("Input file : ", input_files.files);
            input_files.files = droppedFiles;
            console.log("Input file 2 : ", input_files.files);
            show_preview(droppedFiles);
            $('.js-uploaded-files-clear').show();
            console.log("Files dropped : %s", droppedFiles.length);

        });
        $('.js-uploaded-files-clear').on('click', clear_uploaded_files);
    }


    var ListFilter = (function(){
        function ListFilter(){
            //this.init();
            console.log("ListFilter instance created");
        };

        ListFilter.prototype.init = function(){
            console.log("ListFilter instance initializing");
            var self;
            $('.js-list-filter').on('keyup', function(event){
                event.stopPropagation();
                var value = this.value.trim().toLowerCase();
                var fieldname = $(this).data('field');
                var target = $("#" + $(this).data('target'));
                
                target.children().filter(function(){
                    self = $(this)
                    self.toggle(self.data(fieldname).toLowerCase().includes(value));
                });
            });

            console.log("ListFilter instance initialized");
        };

        ListFilter.prototype.filter = function(ctx, filter_field, value_list){
            if(!ctx || !filter_field || !value_list || value_list.length == 0){
                console.log("Filter called with missing argumtent");
                return;
            }
            console.log("Filtering started");
            $(".filterable", ctx).each(function(index, element){
                let filter_value = this.getAttribute(filter_field);
                console.log(" Filter Field = \"%s\" - Filter Value = \"%s\" - Value List = [\"%s\"]", filter_field ,filter_value, value_list)
                $(this).toggle(value_list.includes(filter_value));
            });
            console.log("Listfilter : filter run with success");
        };

        ListFilter.prototype.reset_filter = function(ctx, container){
            if(!ctx || !container){
                console.log(" Reset Filter called with missing context");
                return;
            }
            $("input:checkbox", ctx).each(function(){
                this.checked = false;
            });
            $(".filterable", container).each(function(index, element){
                $(this).show();
            });
            console.log("Listfilter : reset run with success");
        };

        return ListFilter;
    })();

    var FileUpload = (function(){
        function FileUpload(){
            this.files = [];
            this.form = undefined;
            this.formData = undefined;
            this.clean = true;
            this.drag_area = $('.drag-area');
            this.file_list_container = $('.file-list');
            this.file_entries = {};
            this.empty_element = $('.no-data', this.file_list_container);
            this.send_btn = $('.js-send-file-upload-btn');
            this.clear_btn = $('.js-file-list-clear-btn');
            //this.init();
        };

        FileUpload.prototype.init = function(){
            var that = this;
            this.clear_btn.on('click', this.clear.bind(this));

            $('.drag-area')
                .on('drop', onDropHandler)
                .on('dragover', onDragOverHandler)
                .on('dragenter', onDragStartHandler)
                .on('dragleave', onDragEndHandler)
        };

        FileUpload.prototype.clear = function() {
            this.files = [];
            this.formData = undefined;
            this.form = undefined;
            this.clean = true;
            //$('.file-entry', this.file_list_container).remove();
            this.file_list_container.empty().append(this.empty_element);
            this.drag_area.removeClass('non-empty');
            this.send_btn.addClass('disabled').prop('disabled',true);
            this.clear_btn.addClass('hidden');
        };

        FileUpload.prototype.isClean = function() {
            return this.clean;
        };

        FileUpload.prototype.setForm = function(form){
            this.form = form;
            this.clean = false;
            return this;
        };

        FileUpload.prototype.setFiles = function(files){
            this.files = files;
            this.clean = false;
            return this;
        };

        FileUpload.prototype.addFile = function(file){
            if(this.files.some(f => f.name == file.name)){
                console.warn("A file with the same name already exists.")
                return this;
            }
            var that = this;
            this.files.push(file);
            var li = $('<li />',{
                id:"file-" + that.files.length,
                'class' : 'file-entry',
                'title': file.name,
            });
            var entry_text = $('<span />', {
                text: file.name
            });
            var entry_remove_btn = $('<button />', {
                class: 'mat-button mat-button-text',
                type: 'button'
            }).append($('<i />', {
                class: 'fas fa-times icon'
            }));
            entry_remove_btn.on('click', function(event){
                event.preventDefault();
                event.stopPropagation();
                that.removeFile([file.name]);
                li.remove();
            });
            li.append(entry_text, entry_remove_btn).appendTo(that.file_list_container);
            $('.no-data', that.file_list_container).remove();
            this.drag_area.addClass('non-empty');
            this.send_btn.removeClass('disabled').prop('disabled',false);
            this.clear_btn.removeClass('hidden');
            this.clean = false;
            return this;
        };

        FileUpload.prototype.removeFile = function(fileNames){
            var old_length = this.files.length;
            this.files = this.files.filter(f => !fileNames.includes(f.name));
            if(this.files.length != old_length && this.files.length < old_length){

                if(this.files.length == 0){
                    this.file_list_container.append(this.empty_element);
                    this.drag_area.removeClass('non-empty');
                    this.send_btn.addClass('disabled').prop('disabled',true);
                    this.clear_btn.addClass('hidden');
                }
                this.clean = false;
            }else{
                console.log("files : %s not removed", fileNames);
                
            }
            
            return this;
        };
        FileUpload.prototype.update = function(){
            if(this.isClean()){
                console.warn("FileUpload can not be updated. formData is already clean.");
                return;
            }
            if(!this.form || !this.files || this.files.length == 0){
                console.warn("FileUpload can not be updated. form or files are missing.");
                return;
            }
            this.formData = new FormData(this.form);
            var that = this;
            this.files.forEach(function(file, index){
                that.formData.append("file_" + index, file, file.name);
            });
            this.clean = true;
            /*
            $(form).serializeArray().forEach(function(input, index){
                formData.append(input.name, input.value);
            });
            */
        };

        FileUpload.prototype.canSend = function(){
            let formValid = typeof this.form != 'undefined';
            let filesValid = typeof this.files != 'undefined';

            return formValid && filesValid && this.files.length > 0;
        };

        FileUpload.prototype.getForm = function() {
            return this.form;
        };

        FileUpload.prototype.getFiles = function() {
            return this.files;
        }

        FileUpload.prototype.getFormDate = function() {
            return this.formData;
        }

        FileUpload.prototype.upload = function(){
            if(!this.canSend()){
                console.error("Files can not be sent. Please check your files form. Files or form are missing.");
                return;
            }
            if(typeof ajax_api.ajax_lang === 'undefined'){
                var errorMsg = "can not upload files. ajax funtion is not defined";
                console.error(errorMsg);
                throw new Error(errorMsg);
            }
            var that = this;
            var options = {
                url : $(this.form).attr('action'),
                type: 'POST',
                enctype : 'multipart/form-data',
                data : this.formData,
                processData : false,
                cache : false,
                contentType : false
            };
            ajax_api.ajax(options).then(function(response){
                var msg = {
                    content : response.message,
                    level : response.status === 'OK'
                }
                notify(msg);
                fileUpload.clear();
                

            }, function(reason){
                console.error("Files could not be uploaded.");
                console.error(reason);
                fileUpload.clear();
            });

        };

        return FileUpload;
    })();

    var PostManager = (function(){
        function PostManager() {
            this.images = null;
            this.form = undefined;
            this.formData = undefined;
            this.input_file = undefined;
            this.drag_area = undefined;
            this.files_container = undefined;
            this.send_btn = undefined;
            this.clear_uploaded_files_btn = undefined;
            this.created_post_container = undefined;
            this.created_post_link = undefined;
            this.supported_formats = ['jpg', 'jpeg', 'png', 'webp'];
            this.post_status = 0;
        };
        PostManager.prototype.init = function(){
            var self = this;
            this.created_product_container = document.querySelector('#created-post-link');
            this.created_product_link = document.querySelector('#created-post-link a');
            this.files_container = document.querySelector('.file-list');
            
            $('.drag-area').on('drag dragstart dragend dragover dragenter drop', function(e){
                e.preventDefault();
                e.stopPropagation();
            }).on('dragover dragenter', function(){
                self.drag_area.classList.add('on-drag');
            }).on('dragleave dragend drop', function(){
                self.drag_area.classList.remove('on-drag');
            }).on('drop', function(e){
                self.images = e.originalEvent.dataTransfer.files;
                self.input_file.files = self.images;
                self.onImagesChanged();
                self.imagesPreview();

            });
            $('#files').on('change', function(e){
                self.images = self.input_file.files;
                self.onImagesChanged();
                self.imagesPreview();
            });
            
            $('.js-uploaded-files-clear').on('click', this.clearImages.bind(this));
            
            $(".js-create-post-btn").on('click', function(e){
                e.preventDefault();
                e.stopPropagation();
                if(post_content){
                    self.upload();
                }
            });
            $(".js-preview-post").on('click', function(e){
                e.preventDefault();
                e.stopPropagation();
                if(post_content){
                    preview_post();
                }
            });
            $(".js-publish-btn").on('click', function(e){
                e.preventDefault();
                e.stopPropagation();
                if(post_content){
                    self.post_status = POST_STATUS_PUBLISH;
                    self.upload();
                }
            });
            $('.js-post-like').on('click', function(e){
                e.stopPropagation();
                let post = this.dataset.post;
                let liked = this.dataset.liked;
                self.add_like(liked, post);
            });

            console.log("PostManager initialized");
        };

        PostManager.prototype.imagesPreview = function(){
            var li;
            var img;
            while(this.files_container.firstChild){
                this.files_container.removeChild(this.files_container.firstChild);
            }
            var f;
            for(var i = 0; i < this.images.length; i++){
                f = this.images[i];
                li = document.createElement('li');
                img = document.createElement('img');
                img.src = URL.createObjectURL(f);
                img.height = 60;
                this.files_container.appendChild(li);
                img.onload = function(){
                    URL.revokeObjectURL(img.src);
                };
                li.classList.add('file-entry');
                li.appendChild(img);
                const info = document.createElement('span');
                info.innerHTML = f.name + " : " + Math.ceil(f.size/1024) + ' KB';
                li.appendChild(info);
            }
            $('.js-uploaded-files-clear').show();
        };

        PostManager.prototype.clearImages = function(){
            while(this.files_container.firstChild){
                this.files_container.removeChild(this.files_container.firstChild);
            }
            this.images = null;
            this.input_file.files = null;
            var li = document.createElement('li');
            var span = document.createElement('span');
            span.innerText = "No images";
            li.appendChild(span);
            this.files_container.appendChild(li);
            this.onImagesChanged();
        };

        PostManager.prototype.clear = function(){
            var inputs = [];
            var title = document.querySelector('#title');
            this.input_file.files = null;
            this.images = null;
            this.onImagesChanged();
        }

        PostManager.prototype.is_update_form = function(){
            let element = document.querySelector('#editor');
            return element != null && element.dataset.action === "update";
        }

        PostManager.prototype.validate = function(){
            // if(this.validators){
            //     return this.validators.every((f)=>f());
            // }
            return true;
        };

        PostManager.prototype.validateTitle = function(){
            var name = document.querySelector('#name');
            var display_name = document.querySelector('#display-name');
            // if(!name || !display_name || !name.value.lenght || !display_name.value.length){
            //     console.log("name & display name errors");
            //     return false;
            // }
            return true;
        };

        PostManager.prototype.onImagesChanged = function(){
            this.drag_area.classList.toggle('active', this.images && (this.images.length > 0));
        };

        PostManager.prototype.validateImages = function(){
            
            if(!this.images  || !this.input_file.files.length){
                console.log(" images errors");
                return false;
            }
            return true;
        };

        PostManager.prototype.onUploadResponse = function(data){
            
            if(!data.success){
                
                return;
            }
            let editor_element = document.querySelector('#editor');
            let link_container = document.getElementById('post-link-container');
            let link = link_container.querySelector('#post-link');
            link.href = data.url;
            link_container.classList.remove('hidden');
            editor_element.dataset.action = "update";
            editor_element.dataset['post'] = data.post.post_uuid;
            
        };

        PostManager.prototype.upload = function(){
            let self = this;
            let csrfmiddlewaretoken = document.querySelector('input[name="csrfmiddlewaretoken"]');
            let title = document.getElementById('title');
            let editor_element = document.getElementById('editor');
            let formData = new FormData();
            formData.append('csrfmiddlewaretoken', csrfmiddlewaretoken.value);
            formData.append('title', title.value);
            formData.append('content', JSON.stringify(post_content));
            formData.append('author', editor_element.dataset.author);
            formData.append('post_status', this.post_status);
            let url = this.is_update_form() ? '/api/update-post/' + editor_element.dataset.post + '/' : '/api/create-post/';
            var options = {
                //url : url,
                type: 'POST',
                method: 'POST',
                enctype : 'multipart/form-data',
                data : formData,
                dataType : 'json',
            };
            let fetch_options = {
                method : 'POST',
                body: formData
            };
            ajax_api.fetch_api(url, fetch_options).then(function(response){
                let msg = {
                    content : response.message,
                    level : response.success
                }
                notify(msg);
                self.onUploadResponse(response);
            }, function(reason){
                console.error("Files could not be uploaded.");
                console.error(reason);
                
            });

        };

        PostManager.prototype.onAddLikeResponse = function(data){
            let post_like = document.querySelector('.post-like');
            let post_like_count = document.querySelector('.post-like-count');
            if(!post_like || !post_like_count){
                return;
            }
            if(data.success){
                post_like_count.innerText = data.likes > 0 ? data.likes : '';
                post_like.dataset.liked = data.liked ? "true" : 'false';
                post_like.dataset.likes = data.likes;
                post_like.title = data.title;
                post_like.classList.toggle('liked', data.liked);
                post_like.classList.toggle('unliked', data.liked);
            }
        };

        PostManager.prototype.add_like = function(liked, post_id){
            let self = this;
            let csrfmiddlewaretoken = document.querySelector('input[name="csrfmiddlewaretoken"]');
            let formData = new FormData();
            formData.append('csrfmiddlewaretoken', csrfmiddlewaretoken.value);
            let url = (liked == "false" ? '/api/add-like/': '/api/remove-like/') + post_id + '/';
            let fetch_options = {
                method : 'POST',
                body: formData
            };
            ajax_api.fetch_api(url, fetch_options).then(function(response){
                self.onAddLikeResponse(response);
            }, function(reason){
                console.error("Files could not be uploaded.");
                console.error(reason);
            });
        };

        return PostManager;

    })();

    var ImageManager = (function(){
        function ImageManager(){
            this.form = undefined;
            this.supported_formats = ['jpg', 'jpeg', 'png', 'webp'];
            this.input_files;
            this.drag_area_selector = undefined;
        }
        ImageManager.prototype.init = function(){
            let self = this;
            this.form = document.getElementById("event-create-form") || document.getElementById("category-create-form");
            let drag_area_selector = this.drag_area_selector || ".drag-area";
            this.drag_areas = document.querySelectorAll(this.drag_area_selector);
            if(!this.form){
                return;
            }
            if(!this.drag_areas){
                return;
            }
            this.input_files = document.querySelectorAll('.files-upload-input');
            if(!this.input_files){
                return;
            }
            $(drag_area_selector).on('drag dragstart dragend dragover dragenter drop', function(e){
                e.preventDefault();
                e.stopPropagation();
            }).on('dragover dragenter', function(){
                this.classList.add('on-drag');
            }).on('dragleave dragend drop', function(){
                this.classList.remove('on-drag');
            }).on('drop', function(e){
                let file_input = document.getElementById(this.dataset.input);
                if(file_input){
                    file_input.files = e.originalEvent.dataTransfer.files;
                    this.classList.add('active');
                    self.imagesPreview(this);
                }
            });
            $('.files-upload-input').on('change', function(e){
                let drag_area = document.getElementById(this.dataset.dragarea);
                if(this.files){
                    drag_area.classList.remove('active');
                }
                self.imagesPreview(drag_area);
            });
            $('.js-uploaded-files-clear').on('click', function(event){
                let files_container = document.getElementById(this.dataset.target);
                while(files_container.firstChild){
                    files_container.removeChild(files_container.firstChild);
                }
                let input = document.getElementById(files_container.dataset.input);
                let drag_area = document.getElementById(this.dataset.dragarea);
                input.files = null;
                let li = document.createElement('li');
                let span = document.createElement('span');
                span.innerText = "No images";
                li.appendChild(span);
                files_container.appendChild(li);
                drag_area.classList.remove('active');
            });
        }
        ImageManager.prototype.imagesPreview = function(drag_area){
            let li;
            let img;
            let input = document.getElementById(drag_area.dataset.input);
            let files_container = drag_area.querySelector('.file-list');
            while(files_container.firstChild){
                files_container.removeChild(files_container.firstChild);
            }
            let f;
            for(let i = 0; i < input.files.length; i++){
                f = input.files[i];
                li = document.createElement('li');
                img = document.createElement('img');
                img.src = URL.createObjectURL(f);
                img.height = 60;
                img.onload = function(){
                    URL.revokeObjectURL(img.src);
                };
                li.classList.add('file-entry');
                li.appendChild(img);
                const info = document.createElement('span');
                info.innerHTML = f.name + " : " + Math.ceil(f.size/1024) + ' KB';
                info.classList.add('padding');
                li.appendChild(info);
                files_container.appendChild(li);
            }
            $('.js-uploaded-files-clear', drag_area).show();
        };

        ImageManager.prototype.clearImages = function(drag_area){
            let files_container = document.querySelector('.file-list', drag_area);
            if(!files_container){
                return;
            }
            while(files_container.firstChild){
                files_container.removeChild(files_container.firstChild);
            }
            let input_file = document.getElementById(drag_area.dataset.input);
            input_file.files = null;
            let li = document.createElement('li');
            let span = document.createElement('span');
            span.innerText = "No images";
            li.appendChild(span);
            files_container.appendChild(li);
            drag_area.classList.remove('active');
        };
        ImageManager.prototype.clear = function(){
            if(this.input_files){
                this.input_files.forEach(function(v,i){
                    this.files = null;
                });
            }
        }

        return ImageManager;
    })();

    var Modal = (function(){
        function Modal(options){
            this.modal = {};
            this.init();
        }
        Modal.prototype.init = function(){
            let that = this;

            $(".js-open-modal").click(function(event){
                if((LOGIN_REQUIRED_KEY in this.dataset) && this.dataset[LOGIN_REQUIRED_KEY] == "1" ){
                    event.stopPropagation();
                    event.preventDefault();
                    notify({"level": "info", "content": this.dataset.message});
                    return false;
                }
                let modal = document.getElementById(this.dataset.target);
                that.modal = modal;
                
                modal.style.display = "flex";
                if(window){
                    $(window).click(function(eventModal){
                        if(eventModal.target == modal){
                            modal.style.display = "none";
                            that.modal = undefined;
                            let inputs = modal.querySelectorAll("input:not([name='csrfmiddlewaretoken']):not([type='hidden']), textarea");
                            let clearables = modal.querySelectorAll('.clearable');
                            if(clearables){
                                clearables.forEach((el) =>{
                                    el.innerText = "";
                                    el.classList.remove('warning', 'danger');
                                });
                            }
                            if(inputs){
                                inputs.forEach(function(el,index){
                                    el.value = "";
                                    el.dataset.update = "";
                                    if(el.type =="file"){
                                        el.files = null;
                                    }
                                    if(el.type == "checkbox" || el.type == "radio"){
                                        el.checked = false;
                                    }
                                });
                            }
                        }
                    });
                }
            });
    
            $(".js-close-modal").click(function(event){
                event.stopPropagation();
                let modal = document.getElementById(this.dataset.target);
                modal.style.display = "none";
                that.modal = undefined;
                let inputs = modal.querySelectorAll("input:not([name='csrfmiddlewaretoken']):not([type='hidden']), textarea");
                let clearables = modal.querySelectorAll('.clearable');
                if(clearables){
                    clearables.forEach((el) =>{
                        el.innerText = "";
                        el.classList.remove('warning', 'danger');
                    });
                }
                if(inputs){
                    inputs.forEach(function(el,index){
                        el.value = "";
                        el.dataset.update = "";
                        if(el.type =="file"){
                            el.files = null;
                        }
                        if(el.type == "checkbox" || el.type == "radio"){
                            el.checked = false;
                        }
                    });
                }
            });
        }
        return Modal;
    })();

    function kiosk_update(event){
        document.getElementById('main-image').src = event.target.src;
        $(".kiosk-image").removeClass('active').filter(event.target).addClass("active");
    }

    function parseHTML(html){
        let template = document.createElement('template');
        template.innerHTML = html;
        return template.content;
    }
    function create_comment(data){
        let author = data.username;
        let created_at = data.date;
        let comment = data.comment;
        let comment_tag = 
    `<li class="margin-bottom">
        <div class="comment">
            <div class="post-header">
                <span class="bold">${author}</span>|<span><i class="fas fa-comment icon"></i> ${created_at}</span>|<span class="js-report-comment" title="report"><i class="far fa-flag icon"></i></span>
            </div>
            <div>
                <p>${comment}</p>
            </div>
        </div>
    </li>`;
    return parseHTML(comment_tag);
    }

    function auto_fetch_comments(post_id, comments_container){
        let post_comment_count = document.getElementById('post-comment-count');
        let post_like_count = document.getElementById('post-like-count');
        let csrfmiddlewaretoken = document.querySelector('input[name="csrfmiddlewaretoken"]');
        function fetch_comments(){
            let last = comments_container.dataset.latest;
            let formData = new FormData();
            formData.append('csrfmiddlewaretoken', csrfmiddlewaretoken.value);
            formData.append('created_at', last);
            let url = '/api/fetch-comments/' + post_id + '/';
            let fetch_options = {
                method : 'POST',
                body: formData
            };
            ajax_api.fetch_api(url, fetch_options).then(function(response){
                if(!response.success || !response.comments){
                    return;
                }
                comments_container.dataset.latest = response.latest;
                post_comment_count.innerText = parseInt(post_comment_count.innerText) + response.comment_count;
                post_like_count.innerText = response.likes;
                response.comments.forEach((c)=>{comments_container.appendChild(create_comment(c))});
            }, function(reason){
                console.error("Files could not be uploaded.");
                console.error(reason);
            });
        }
        return setInterval(fetch_comments, COMMENT_FETCH_INTERVAL);
    }
    

    function can_leave(){
        isDirty = false;
        //window.onbeforeunload = null;
    }

    function askConfirmation(event){
        let ret = undefined;
        if(isDirty){
            if(event){
                event.preventDefault();
                event.returnValue = "You have unsubmitted data. Leaving this page will lost the data."
            }
            ret =  "You have unsubmitted data. Leaving this page will lost the data.";
        }else{
            delete event['returnValue'];
        }
        
        return ret;
    }

    function prevent_leaving(){
        isDirty = true;
        //window.onbeforeunload = onbeforeunload;
    }

    $(document).ready(function(){
        if(window){
            window.notify = notify;
        }
        let modal = new Modal();
        image_preview();
        create_editor();
        let imageManager = new ImageManager();
        imageManager.init();
        notification_wrapper = $('#notifications-wrapper');
        messages = $('#messages', notification_wrapper);
        //onDragInit();
        notify_init(notification_wrapper, messages);
        var listfilter = new ListFilter();
        Filter.init();
        fileUpload = new FileUpload();
        postManager = new PostManager();
        postManager.init();
        let comments = document.getElementById('comments');
        if(comments){
            auto_fetch_comments(comments.dataset.post, comments);
        }
        /*
        $('.js-user-search').on('keyup', function(event){
            event.stopPropagation();
            var query = $(this).val();
            query = query.trim()
            if(query.length == 0 ){
                return;
            }
            var options = {
                url:'/api/user-search/',
                type: 'GET',
                data : {'search': query},
                dataType: 'json'
            };
            if(scheduled_query){
                clearTimeout(scheduled_query);
            }
            scheduled_query = setTimeout(userSearch, query_delay, options);
        });
        
        $('.js-need-confirmation').on('click', function(event){
            return confirm("This action is irreversible. Do you to want proceed ?");
        });
    
        $('.js-user-selector').on('click', 'li', function(){
            let target = $(this);
            $('#members').append($('<option/>', {'value': target.data('id'), 'selected': true, 'text': target.text()}));
            target.appendTo('#selected-members');
        });
        $('#selected-members').on('click', 'li', function(){
            let target = $(this);
            target.appendTo('.js-user-selector');
            $('#members option').filter(function(){
                return this.value == target.data('id');
            }).remove();
            
        });
        */
        
        $('.collapsible .toggle').on('click', function(event){
            var parent = $(this).parent();
            var target = $('.' + this.getAttribute('data-toggle'), parent);
            $('input', parent).val('');
            
            target.toggle();
        });
        $('.js-filter-btn').on('click', function(event){
            var ctx = $('#' + this.getAttribute('data-context'));
            var input_name = this.getAttribute('data-input-name');
            var container = $('#' + this.getAttribute('data-container'));
            var filter_field = this.getAttribute("data-filter-field");
            var value_list = [];
            $("input:checked[name=\"" + input_name + "\"]", ctx).each(function(){
                value_list.push(this.getAttribute("data-value"));
            });
            listfilter.filter(container, filter_field, value_list);
        });

        $('.js-filter-reset-btn').on('click', function(event){
            var ctx = $('#' + this.getAttribute('data-context'));
            var container = $('#' + this.getAttribute('data-container'));
            listfilter.reset_filter(ctx, container);
        });

        $('#file-upload-form').on('submit', function(event){
            event.preventDefault();
            event.stopPropagation();
            fileUpload.setForm(this);
            fileUpload.update();
            fileUpload.upload();
            //return false;
            
        });
        $('.js-select-image').on('click', kiosk_update);
        $('.js-select-image').first().click();
        $(".limited-input").on("keyup", function(event){
            event.stopPropagation();
            input_check_max_limit(this);
        });
        $('.js-dialog-open').on('click', function(){
            var target = $('#' + $(this).data('target'));
            target.show();
        });

        
        $('.js-dialog-close').on('click', function(){
            var target = $("#" + $(this).data('target'));
            target.hide();
            //var parent = $(this).parents('.dialog').hide();
            $('input[type!="hidden"]', target).val('');
        });
        $('.js-reveal-btn, .js-revealable-hide').on('click', function(){
            var target = $($(this).data('target')).parent();
            $('.js-revealable', target).toggleClass('hidden');
        });
        $('.js-clear-input').on('click', function(){
            
            var target = $('#' + $(this).data('target'));
            $('input[type!=checkbox]', target).val('');
            $('input:checkbox', target).val('').prop('checked', '');
        });
        var selectable_list = $(".js-selectable");
        var activable_list = $(".js-activable");
        var select_all = $('.js-select-all');
        selectable_list.on('click', function(){
            var is_selected = selectable_list.is(function (el) {
                return this.checked;
            });
            
            var selected_all = selectable_list.is(function (el) {
                return !this.checked;
            });
            select_all.prop('checked', !selected_all);
            activable_list.prop('disabled', !is_selected);
        });

        select_all.on('click', function(){
            selectable_list.prop('checked', this.checked);
            activable_list.prop('disabled', !this.checked);
        });

        filter_form = $('#filter-form');
        $('#filter-form').on('submit', function(event){
            $('input[name="csrfmiddlewaretoken"]').prop('disabled', true);
            let reload = clean_form_before_submit(this);
            if(reload){
                event.stopPropagation();
                event.preventDefault();
                window.location.search = "";
                window.location = location.pathname;
            }
        });
        $('.js-pagination').on('click', function(event){
            
            if(filter_form.length != 0){
                event.preventDefault();
                event.stopPropagation();
                
                var page = $(event.target).data('page');
                let input = element_utils.create_element_api({'element': 'input', 'options': {'cls': 'filter-input', 'name': 'page', 'value': page,'type':'text','id':'page'}});
                //input.appendTo(filter_form);
                filter_form.append(input)
                filter_form.submit();
            }
            

        });
        
        $('.js-custom-input .input-value').on('click', function(event){
            $(this).toggle();
            $('.input-edit-wrapper', $(this).parent()).toggle();
        });
        
        $('.js-custom-input input').on('keyup change', function(event){
            var $el = $(this);
            $el.parent().siblings('.input-value').html($el.val());
        });
        
        $('.js-custom-input .js-edit-close').on('click', function(event){
            var $el = $(this).siblings('input');
            $el.parent().siblings('.input-value').html($el.val());
            $(this).parent().toggle();
        });
        $('.js-menu').on('click', function(){
            $('#menu-overlay-label').click();
            $('.js-menu-close').show();
            $(this).hide();
    
        });
        $('.js-menu-close').on('click', function(){

            $('#menu-overlay-label').click();
            $('.js-menu').show();
            $(this).hide();
        });
        /*
        $('.js-action-abtest').on('click', function(e){
            track_action(this);
        });
        */
       console.log("Commons module loaded");
    });
});
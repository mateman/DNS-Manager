/*
Copyright (c) 2003-2011, CKSource - Frederico Knabben. All rights reserved.
For licensing, see LICENSE.html or http://ckeditor.com/license
*/


CKEDITOR.editorConfig = function( config )
	{
	   // Define changes to default configuration here. For example:
	   config.language = 'es';
	   //config.skin = 'v2';
	   //config.removePlugins =  'elementspath,enterkey,entities,forms,pastefromword,htmldataprocessor,specialchar' ;
	   //config.removePlugins =  'elementspath,enterkey,entities,forms,pastefromword,htmldataprocessor,specialchar,horizontalrule,wsc' ;
	   config.skin = 'office2003';
	   //config.toolbar = 'Basic';
	   CKEDITOR.config.toolbar = [
       ['NewPage','Preview','Print','-','Templates'],
	   ['Cut','Copy','Paste','PasteText','PasteFromWord','-','Undo','Redo'],
	   ['Find','Replace','-','SelectAll','-','SpellChecker','Scayt'], 
	   ['Form','Checkbox','Radio','TextField','Textarea','Selection','Button','ImageButton','HiddenField'],
	   ['Link','Unlink','Anchor'],
	   '/',
	   ['Bold','Italic','Underline','Strike','Subscript','Superscript','-','RemoveFormat'],
	   ['NumberedList','BulletedList','-','Outdent','Indent','-','Blockquote','CreateDiv','-','JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock','-','BidiLtr','BidiRtl'],
	   ['Image','Flash','Table','HorizontalRule','Smiley','SpecialChar','PageBreak','Iframe'],
	   '/',
	   ['Source','Styles','Format','Font','FontSize'],['TextColor','BGColor'],['ShowBlocks','Maximize'],
	] ;
	};
	

/*
config.toolbar = 'Full';
 
config.toolbar_Full =
[
	{ name: 'document', items : [ 'Source','-','Save','NewPage','DocProps','Preview','Print','-','Templates' ] },
	{ name: 'clipboard', items : [ 'Cut','Copy','Paste','PasteText','PasteFromWord','-','Undo','Redo' ] },
	{ name: 'editing', items : [ 'Find','Replace','-','SelectAll','-','SpellChecker', 'Scayt' ] },
	{ name: 'forms', items : [ 'Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton', 
 
         'HiddenField' ] },
	'/',
	{ name: 'basicstyles', items : [ 'Bold','Italic','Underline','Strike','Subscript','Superscript','-','RemoveFormat' ] },
	{ name: 'paragraph', items : [ 'NumberedList','BulletedList','-','Outdent','Indent','-','Blockquote','CreateDiv','-
 
        ','JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock','-','BidiLtr','BidiRtl' ] },
	{ name: 'links', items : [ 'Link','Unlink','Anchor' ] },
	{ name: 'insert', items : [ 'Image','Flash','Table','HorizontalRule','Smiley','SpecialChar','PageBreak','Iframe' ] },
	'/',
	{ name: 'styles', items : [ 'Styles','Format','Font','FontSize' ] },
	{ name: 'colors', items : [ 'TextColor','BGColor' ] },
	{ name: 'tools', items : [ 'Maximize', 'ShowBlocks','-','About' ] }
];
 
config.toolbar_Basic =
[
	['Bold', 'Italic', '-', 'NumberedList', 'BulletedList', '-', 'Link', 'Unlink','-','About']
];
*/

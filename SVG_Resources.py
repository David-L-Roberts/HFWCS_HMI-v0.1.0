class svgElement:
    __arrow_colour = "stroke-indigo-500/60"
    # __arrow_colour = "bg-gradient-to-t from-indigo-500 via-purple-500 to-pink-500 bg-clip-content"
    __stroke_width = "3px"

    arrow_down = f'''
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" 
        class="w-[100px] h-[100px] {__arrow_colour} stroke-[{__stroke_width}]">
        <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 13.5L12 21m0 0l-7.5-7.5M12 21V3" />
        </svg>'''
    arrow_up = f'''
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" 
        class="w-[100px] h-[100px] {__arrow_colour} stroke-[{__stroke_width}]">
        <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 10.5L12 3m0 0l7.5 7.5M12 3v18" />
        </svg>'''
    arrow_left = f'''
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" 
        class="w-[100px] h-[100px] {__arrow_colour} stroke-[{__stroke_width}]">
        <path stroke-linecap="round" stroke-linejoin="round" d="M9 15L3 9m0 0l6-6M3 9h12a6 6 0 010 12h-3" />
        </svg>'''
    arrow_right = f'''
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" 
        class="w-[100px] h-[100px] {__arrow_colour} stroke-[{__stroke_width}]">
        <path stroke-linecap="round" stroke-linejoin="round" d="M15 15l6-6m0 0l-6-6m6 6H9a6 6 0 000 12h3" />
        </svg>'''
    
    square_stop = f'''
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" 
        class="w-[100px] h-[100px] {__arrow_colour} stroke-[{__stroke_width}]">
        <path stroke-linecap="round" stroke-linejoin="round" d="M5.25 7.5A2.25 2.25 0 017.5 5.25h9a2.25 2.25 0 012.25 2.25v9a2.25 2.25 0 01-2.25 2.25h-9a2.25 2.25 0 01-2.25-2.25v-9z" />
        </svg>'''


    
    

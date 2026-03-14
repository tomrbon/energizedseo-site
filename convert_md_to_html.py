#!/usr/bin/env python3
"""
Convert markdown blog posts to HTML with proper styling.
"""

import os
import re
import html
from pathlib import Path

# Simple markdown to HTML converter
def parse_frontmatter(content):
    """Extract YAML frontmatter from markdown."""
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        return {}, content
    
    frontmatter = {}
    for line in match.group(1).strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            # Handle arrays
            if value.startswith('[') and value.endswith(']'):
                value = [v.strip().strip('"').strip("'") for v in value[1:-1].split(',')]
            frontmatter[key] = value
    
    return frontmatter, match.group(2).strip()

def markdown_to_html(md_content):
    """Convert markdown content to HTML."""
    html_content = md_content
    
    # Escape HTML first (but we'll unescape common tags)
    # Actually, let's process step by step
    
    # Headers (must be before other processing)
    html_content = re.sub(r'^###### (.+)$', r'<h6>\1</h6>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^##### (.+)$', r'<h5>\1</h5>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
    
    # Bold and italic
    html_content = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', html_content)
    html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)
    html_content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html_content)
    
    # Code blocks (must be before inline code)
    def replace_code_block(match):
        lang = match.group(1) or ''
        code = html.escape(match.group(2))
        return f'<pre class="bg-gray-100 p-4 rounded-lg overflow-x-auto my-4"><code class="language-{lang}">{code}</code></pre>'
    
    html_content = re.sub(r'```(\w*)\n(.*?)```', replace_code_block, html_content, flags=re.DOTALL)
    
    # Inline code
    html_content = re.sub(r'`([^`]+)`', r'<code class="bg-gray-100 px-1 rounded">\1</code>', html_content)
    
    # Images
    html_content = re.sub(r'!\[(.+?)\]\((.+?)\)', r'<img src="\2" alt="\1" class="max-w-full h-auto rounded-lg my-4">', html_content)
    
    # Links
    html_content = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2" class="text-primary-600 hover:text-primary-700 underline">\1</a>', html_content)
    
    # Tables
    def replace_table(match):
        table_text = match.group(0)
        lines = table_text.strip().split('\n')
        if len(lines) < 3:
            return table_text
        
        # Remove separator line
        lines = [l for l in lines if not re.match(r'^[\-\| ]+$', l)]
        
        if len(lines) < 2:
            return table_text
        
        html_table = '<div class="overflow-x-auto my-4"><table class="min-w-full border border-gray-200">'
        
        # Header
        headers = [cell.strip() for cell in lines[0].split('|') if cell.strip()]
        html_table += '<thead class="bg-gray-50"><tr>'
        for h in headers:
            html_table += f'<th class="border border-gray-200 px-4 py-2 text-left font-semibold">{h}</th>'
        html_table += '</tr></thead>'
        
        # Body
        html_table += '<tbody>'
        for row in lines[1:]:
            cells = [cell.strip() for cell in row.split('|') if cell.strip()]
            if cells:
                html_table += '<tr>'
                for cell in cells:
                    html_table += f'<td class="border border-gray-200 px-4 py-2">{cell}</td>'
                html_table += '</tr>'
        html_table += '</tbody></table></div>'
        
        return html_table
    
    # Match tables (lines with | characters)
    html_content = re.sub(r'^(?:\|.+\|\n)+', replace_table, html_content, flags=re.MULTILINE)
    
    # Blockquotes
    html_content = re.sub(r'^> (.+)$', r'<blockquote class="border-l-4 border-primary-500 pl-4 py-2 my-4 bg-gray-50 italic">\1</blockquote>', html_content, flags=re.MULTILINE)
    
    # Unordered lists
    lines = html_content.split('\n')
    result = []
    in_list = False
    for i, line in enumerate(lines):
        if re.match(r'^[-*] (.+)$', line):
            if not in_list:
                result.append('<ul class="list-disc list-inside my-4">')
                in_list = True
            item = re.sub(r'^[-*] (.+)$', r'<li>\1</li>', line)
            result.append(item)
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            result.append(line)
    if in_list:
        result.append('</ul>')
    html_content = '\n'.join(result)
    
    # Ordered lists
    lines = html_content.split('\n')
    result = []
    in_list = False
    for i, line in enumerate(lines):
        if re.match(r'^\d+\. (.+)$', line):
            if not in_list:
                result.append('<ol class="list-decimal list-inside my-4">')
                in_list = True
            item = re.sub(r'^\d+\. (.+)$', r'<li>\1</li>', line)
            result.append(item)
        else:
            if in_list:
                result.append('</ol>')
                in_list = False
            result.append(line)
    if in_list:
        result.append('</ol>')
    html_content = '\n'.join(result)
    
    # Horizontal rules
    html_content = re.sub(r'^---$', '<hr class="my-8 border-gray-200">', html_content, flags=re.MULTILINE)
    
    # Paragraphs - wrap remaining text blocks
    # Split by double newlines and wrap non-tagged content
    parts = re.split(r'\n\n+', html_content)
    wrapped = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        # Skip if already wrapped in block-level tags
        if re.match(r'^<(h[1-6]|ul|ol|pre|table|blockquote|hr|div)', part):
            wrapped.append(part)
        elif part.endswith('</ul>') or part.endswith('</ol>') or part.endswith('</pre>'):
            wrapped.append(part)
        else:
            wrapped.append(f'<p class="mb-4">{part}</p>')
    
    html_content = '\n'.join(wrapped)
    
    return html_content

def generate_html_page(frontmatter, content_html, template_path):
    """Generate complete HTML page with template."""
    
    title = frontmatter.get('title', 'Blog Post')
    description = frontmatter.get('description', '')
    date = frontmatter.get('date', '')
    categories = frontmatter.get('categories', [])
    tags = frontmatter.get('tags', [])
    
    # Generate category/tag spans
    cat_spans = ''
    for cat in categories:
        cat_spans += f'<span class="px-3 py-1 bg-primary-100 text-primary-700 text-xs font-semibold rounded-full">{cat}</span> '
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{html.escape(description)}">
    <title>{html.escape(title)} | EnergizedSEO</title>
    
    <!-- Preconnect for performance -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap">
    
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Custom Tailwind Config -->
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['Inter', 'system-ui', 'sans-serif'],
                    }},
                    colors: {{
                        primary: {{
                            50: '#fef7ee',
                            100: '#feefdc',
                            200: '#fdd9b0',
                            300: '#fbb975',
                            400: '#f78d2f',
                            500: '#f36f0b',
                            600: '#e05705',
                            700: '#b94209',
                            800: '#94360e',
                            900: '#782f0e',
                        }},
                        accent: {{
                            50: '#f5f3ff',
                            100: '#ede9fe',
                            200: '#ddd6fe',
                            300: '#c4b5fd',
                            400: '#a78bfa',
                            500: '#8b5cf6',
                            600: '#7c3aed',
                            700: '#6d28d9',
                            800: '#5b21b6',
                            900: '#4c1d95',
                        }}
                    }}
                }}
            }}
        }}
    </script>
    
    <!-- Custom CSS -->
    <link rel="stylesheet" href="/css/styles.css">
    
    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⚡</text></svg>">
    
    <style>
        .prose h1 {{ font-size: 2.5rem; font-weight: 800; margin-bottom: 1.5rem; color: #1f2937; }}
        .prose h2 {{ font-size: 2rem; font-weight: 700; margin-top: 2.5rem; margin-bottom: 1rem; color: #1f2937; }}
        .prose h3 {{ font-size: 1.5rem; font-weight: 600; margin-top: 2rem; margin-bottom: 0.75rem; color: #1f2937; }}
        .prose h4 {{ font-size: 1.25rem; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.5rem; color: #1f2937; }}
        .prose p {{ margin-bottom: 1.25rem; line-height: 1.75; color: #374151; }}
        .prose a {{ color: #f36f0b; text-decoration: underline; }}
        .prose a:hover {{ color: #e05705; }}
        .prose ul, .prose ol {{ margin-bottom: 1.25rem; padding-left: 1.5rem; }}
        .prose li {{ margin-bottom: 0.5rem; }}
        .prose blockquote {{ border-left: 4px solid #f36f0b; padding-left: 1rem; font-style: italic; background: #f9fafb; padding: 1rem; margin: 1.5rem 0; }}
        .prose code {{ background: #f3f4f6; padding: 0.2rem 0.4rem; border-radius: 0.25rem; font-size: 0.875em; }}
        .prose pre {{ background: #f3f4f6; padding: 1rem; border-radius: 0.5rem; overflow-x: auto; margin: 1.5rem 0; }}
        .prose pre code {{ background: transparent; padding: 0; }}
        .prose img {{ max-width: 100%; height: auto; border-radius: 0.5rem; margin: 1.5rem 0; }}
        .prose table {{ width: 100%; border-collapse: collapse; margin: 1.5rem 0; }}
        .prose th, .prose td {{ border: 1px solid #e5e7eb; padding: 0.75rem; text-align: left; }}
        .prose th {{ background: #f9fafb; font-weight: 600; }}
    </style>
</head>
<body class="font-sans antialiased bg-white text-gray-900">
    <!-- Navigation -->
    <nav class="fixed top-0 w-full bg-white/95 backdrop-blur-sm border-b border-gray-100 z-50" role="navigation" aria-label="Main navigation">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-20">
                <div class="flex items-center space-x-3">
                    <a href="/" class="flex items-center space-x-3">
                        <span class="text-4xl" aria-hidden="true">⚡</span>
                        <span class="text-2xl font-bold bg-gradient-to-r from-primary-600 to-accent-600 bg-clip-text text-transparent">EnergizedSEO</span>
                    </a>
                </div>
                
                <!-- Desktop Navigation -->
                <div class="hidden md:flex items-center space-x-8">
                    <a href="/#features" class="text-gray-600 hover:text-primary-600 transition-colors font-medium">Features</a>
                    <a href="/#process" class="text-gray-600 hover:text-primary-600 transition-colors font-medium">How It Works</a>
                    <a href="/blog" class="text-primary-600 font-semibold">Blog</a>
                    <a href="/#pricing" class="text-gray-600 hover:text-primary-600 transition-colors font-medium">Pricing</a>
                    <a href="/#testimonials" class="text-gray-600 hover:text-primary-600 transition-colors font-medium">Results</a>
                    <a href="/#contact" class="bg-gradient-to-r from-primary-500 to-primary-600 text-white px-6 py-3 rounded-full font-semibold hover:from-primary-600 hover:to-primary-700 transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-0.5">Get Free Mockup</a>
                </div>
                
                <!-- Mobile menu button -->
                <button id="mobile-menu-btn" class="md:hidden p-2 rounded-lg hover:bg-gray-100" aria-label="Toggle menu">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
                    </svg>
                </button>
            </div>
        </div>
        
        <!-- Mobile Navigation -->
        <div id="mobile-menu" class="hidden md:hidden bg-white border-t border-gray-100">
            <div class="px-4 py-4 space-y-3">
                <a href="/#features" class="block text-gray-600 hover:text-primary-600 py-2 font-medium">Features</a>
                <a href="/#process" class="block text-gray-600 hover:text-primary-600 py-2 font-medium">How It Works</a>
                <a href="/blog" class="block text-primary-600 font-semibold">Blog</a>
                <a href="/#pricing" class="block text-gray-600 hover:text-primary-600 py-2 font-medium">Pricing</a>
                <a href="/#testimonials" class="block text-gray-600 hover:text-primary-600 py-2 font-medium">Results</a>
                <a href="/#contact" class="block bg-gradient-to-r from-primary-500 to-primary-600 text-white text-center px-6 py-3 rounded-full font-semibold">Get Free Mockup</a>
            </div>
        </div>
    </nav>

    <!-- Article Header -->
    <section class="pt-32 pb-16 bg-gradient-to-br from-primary-50 via-white to-accent-50">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center">
                <div class="flex flex-wrap justify-center gap-2 mb-6">
                    {cat_spans}
                </div>
                <h1 class="text-4xl md:text-5xl font-extrabold text-gray-900 mb-6">
                    {html.escape(title)}
                </h1>
                <p class="text-xl text-gray-600 leading-relaxed mb-4">
                    {html.escape(description)}
                </p>
                <div class="text-sm text-gray-500">
                    Published: {date}
                </div>
            </div>
        </div>
    </section>

    <!-- Article Content -->
    <article class="py-16 bg-white">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="prose prose-lg max-w-none">
                {content_html}
            </div>
        </div>
    </article>

    <!-- CTA Section -->
    <section class="py-20 bg-gradient-to-br from-primary-500 to-accent-600">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 class="text-4xl md:text-5xl font-extrabold text-white mb-6">
                Ready to Implement These Strategies?
            </h2>
            <p class="text-xl text-white/90 mb-8 max-w-2xl mx-auto">
                Get a professional website with built-in SEO that implements these best practices from day one. Start ranking higher today.
            </p>
            <a href="/#contact" class="inline-block bg-white text-primary-600 px-10 py-4 rounded-full font-bold text-lg hover:bg-gray-100 transition-all shadow-2xl">
                Get Your Free Mockup
            </a>
        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-900 text-white py-12">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid md:grid-cols-4 gap-8">
                <div class="col-span-2">
                    <div class="flex items-center space-x-3 mb-4">
                        <span class="text-4xl">⚡</span>
                        <span class="text-2xl font-bold">EnergizedSEO</span>
                    </div>
                    <p class="text-gray-400 max-w-md">Professional websites with built-in SEO for local businesses. Get more customers on autopilot.</p>
                </div>
                <div>
                    <h3 class="font-semibold mb-4">Navigation</h3>
                    <ul class="space-y-2 text-gray-400">
                        <li><a href="/#features" class="hover:text-white transition-colors">Features</a></li>
                        <li><a href="/#process" class="hover:text-white transition-colors">How It Works</a></li>
                        <li><a href="/blog" class="hover:text-white transition-colors">Blog</a></li>
                        <li><a href="/#pricing" class="hover:text-white transition-colors">Pricing</a></li>
                    </ul>
                </div>
                <div>
                    <h3 class="font-semibold mb-4">Contact</h3>
                    <ul class="space-y-2 text-gray-400">
                        <li><a href="/#contact" class="hover:text-white transition-colors">Get Free Mockup</a></li>
                        <li><a href="/#faq" class="hover:text-white transition-colors">FAQ</a></li>
                    </ul>
                </div>
            </div>
            <div class="border-t border-gray-800 mt-12 pt-8 text-center text-gray-400">
                <p>&copy; 2026 EnergizedSEO. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <!-- Mobile Menu Script -->
    <script>
        document.getElementById('mobile-menu-btn').addEventListener('click', function() {{
            const menu = document.getElementById('mobile-menu');
            menu.classList.toggle('hidden');
        }});
    </script>
</body>
</html>
'''

def main():
    posts_dir = Path(os.path.expanduser('~/Code/energized-seo-tool/site/content/posts'))
    blog_dir = Path(os.path.expanduser('~/Code/energized-seo-tool/site/blog'))
    
    # Create blog directory
    blog_dir.mkdir(exist_ok=True)
    
    # Process all markdown files
    md_files = sorted(posts_dir.glob('*.md'))
    
    print(f"Found {len(md_files)} markdown files to convert")
    
    for md_file in md_files:
        print(f"Processing: {md_file.name}")
        
        # Read markdown content
        content = md_file.read_text(encoding='utf-8')
        
        # Parse frontmatter
        frontmatter, md_content = parse_frontmatter(content)
        
        # Convert markdown to HTML
        html_content = markdown_to_html(md_content)
        
        # Generate complete HTML page
        html_page = generate_html_page(frontmatter, html_content, None)
        
        # Create output filename (slug.html)
        slug = md_file.stem  # filename without extension
        output_file = blog_dir / f"{slug}.html"
        
        # Write HTML file
        output_file.write_text(html_page, encoding='utf-8')
        
        print(f"  → Created: {output_file.name}")
    
    print(f"\nConversion complete! {len(md_files)} HTML files created in {blog_dir}")

if __name__ == '__main__':
    main()

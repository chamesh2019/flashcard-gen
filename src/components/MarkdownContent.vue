<template>
    <div class="markdown-content" v-html="renderedMarkdown"></div>
</template>

<script setup>
import { computed } from 'vue';
import { marked } from 'marked';

const props = defineProps({
    content: {
        type: String,
        required: true
    }
});

const renderedMarkdown = computed(() => {
    if (!props.content) return '';
    
    // Configure marked options for security and formatting
    marked.setOptions({
        breaks: true,
        gfm: true,
    });
    
    // Parse markdown to HTML
    return marked(props.content);
});
</script>

<style scoped>
.markdown-content {
    word-wrap: break-word;
    overflow-wrap: break-word;
    max-height: 200px;
    overflow-y: auto;
}

/* Markdown element styling */
.markdown-content :deep(h1),
.markdown-content :deep(h2),
.markdown-content :deep(h3),
.markdown-content :deep(h4),
.markdown-content :deep(h5),
.markdown-content :deep(h6) {
    margin: 0.5rem 0;
    line-height: 1.3;
}

.markdown-content :deep(h1) {
    font-size: 1.5rem;
    font-weight: 700;
}

.markdown-content :deep(h2) {
    font-size: 1.3rem;
    font-weight: 700;
}

.markdown-content :deep(h3) {
    font-size: 1.1rem;
    font-weight: 600;
}

.markdown-content :deep(p) {
    margin: 0.5rem 0;
    line-height: 1.5;
}

.markdown-content :deep(ul),
.markdown-content :deep(ol) {
    margin: 0.5rem 0;
    padding-left: 1.5rem;
}

.markdown-content :deep(li) {
    margin: 0.25rem 0;
    line-height: 1.5;
}

.markdown-content :deep(code) {
    background-color: rgba(0, 0, 0, 0.1);
    padding: 0.2rem 0.4rem;
    border-radius: 3px;
    font-family: 'Courier New', monospace;
    font-size: 0.9em;
}

.markdown-content :deep(pre) {
    background-color: rgba(0, 0, 0, 0.05);
    padding: 0.75rem;
    border-radius: 4px;
    overflow-x: auto;
    margin: 0.5rem 0;
}

.markdown-content :deep(pre code) {
    background-color: transparent;
    padding: 0;
}

.markdown-content :deep(blockquote) {
    border-left: 4px solid currentColor;
    padding-left: 1rem;
    margin: 0.5rem 0;
    opacity: 0.8;
}

.markdown-content :deep(a) {
    color: #4285F4;
    text-decoration: none;
}

.markdown-content :deep(a:hover) {
    text-decoration: underline;
}

.markdown-content :deep(hr) {
    margin: 1rem 0;
    border: none;
    border-top: 1px solid currentColor;
    opacity: 0.3;
}

.markdown-content :deep(img) {
    max-width: 100%;
    height: auto;
    border-radius: 4px;
}

.markdown-content :deep(table) {
    border-collapse: collapse;
    width: 100%;
    margin: 0.5rem 0;
    font-size: 0.9rem;
}

.markdown-content :deep(th),
.markdown-content :deep(td) {
    border: 1px solid currentColor;
    padding: 0.5rem;
    text-align: left;
    opacity: 0.9;
}

.markdown-content :deep(th) {
    background-color: rgba(0, 0, 0, 0.05);
    font-weight: 600;
}
</style>

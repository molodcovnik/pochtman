from jinja2 import Template


class CodeRenderService:
    """Класс рендера кода"""

    @staticmethod
    def get_html_code(temp_name, fields):
        template = Template("""
    <pre>
    <code class="code-result">
<span class="h-tag">&lt;div</span> <span class="h-atr">class=</span><span class="h-str">&quot;{{temp_name}}&quot;</span><span class="h-tag">&gt;</span>
    <span class="h-tag">&lt;form</span> <span class="h-atr">action=</span><span class="h-str">"#"</span> <span class="h-atr">class=</span><span class="h-str">"form"</span><span class="h-atr"> method=</span><span class="h-str">"post"</span><span class="h-tag">&gt;</span>{% for field in fields %}
        <span class="h-tag">&lt;div</span> <span class="h-atr">class=</span><span class="h-str">"field-wrapper {{field.field_name | lower}}"</span><span class="h-tag">></span>
            <span class="h-tag">&lt;label</span> <span class="h-atr">for=</span><span class="h-str">"{{field.field_name|lower}}"</span> <span class="h-atr">class=</span><span class="h-str">"form__label"</span><span class="h-tag">></span>{{field.field_name}}<span class="h-tag">&lt;/label&gt;</span>{% if field.field_type == "EMAIL" %}
            <span class="h-tag">&lt;input</span> <span class="h-atr">type=</span><span class="h-str">"email"</span> <span class="h-atr">id=</span><span class="h-str">"{{field.field_name|lower}}"</span> <span class="h-atr">class=</span><span class="h-str">&quot;form__input&quot;</span> <span class="h-atr">name=</span><span class="h-str">"{{field.field_name|lower}}"</span><span class="h-tag">&gt;</span>{% elif field.field_type == "DATE" %}
            <span class="h-tag">&lt;input</span> <span class="h-atr">type=</span><span class="h-str">"date"</span> <span class="h-atr">id=</span><span class="h-str">"{{field.field_name|lower}}"</span> <span class="h-atr">class=</span><span class="h-str">&quot;form__input&quot;</span> <span class="h-atr">name=</span><span class="h-str">"{{field.field_name|lower}}"</span><span class="h-tag">&gt;</span>{% elif field.field_type == "BOOLEAN" %}
            <span class="h-tag">&lt;input</span> <span class="h-atr">type=</span><span class="h-str">"checkbox"</span> <span class="h-atr">id=</span><span class="h-str">"{{field.field_name|lower}}"</span> <span class="h-atr">class=</span><span class="h-str">&quot;form__input&quot;</span> <span class="h-atr">name=</span><span class="h-str">"{{field.field_name|lower}}"</span><span class="h-tag">&gt;</span>{% else %}
            <span class="h-tag">&lt;input</span> <span class="h-atr">type=</span><span class="h-str">"text"</span> <span class="h-atr">id=</span><span class="h-str">"{{field.field_name|lower}}"</span> <span class="h-atr">class=</span><span class="h-str">&quot;form__input&quot;</span> <span class="h-atr">name=</span><span class="h-str">"{{field.field_name|lower}}"</span><span class="h-tag">&gt;</span>{% endif %}
        <span class="h-tag">&lt;/div&gt;</span>{% endfor %}
        <span class="h-tag">&lt;div</span> <span class="h-atr">class=</span><span class="h-str">&quot;send-btn&quot;</span><span class="h-tag">&gt;</span>
            <span class="h-tag">&lt;button</span> <span class="h-atr">class=</span><span class="h-str">&quot;btn&quot;</span> <span class="h-atr">type=</span><span class="h-str">&quot;submit&quot;</span><span class="h-tag">&gt;</span>Отправить<span class="h-tag">&lt;/button&gt;</span>
        <span class="h-tag">&lt;/div&gt;</span>
    <span class="h-tag">&lt;/form&gt;</span>
<span class="h-tag">&lt;/div&gt;</span>
</code>
</pre>""")
        code = template.render(temp_name=temp_name, fields=fields)
        return code

    @staticmethod
    def get_js_code(fields, template_id, domain):
        js_template = Template("""<pre>
<code class="js-code">
<span class="js-keyword">const</span> form = document.<span class="js-function">querySelector</span>(<span class="js-body-str">'.form'</span>);

form.<span class="js-function">onsubmit</span> = <span class="js-keyword">async</span> (e) => {
    e.<span class="js-function">preventDefault</span>();{% for field in fields %}{% if field.field_type == "BOOLEAN" %}
    <span class="js-keyword">const</span> {{field.field_name|lower}} = document.<span class="js-function">querySelector</span>(<span class="js-body-str">'#{{field.field_name|lower}}'</span>).checked;{% else %}
    <span class="js-keyword">const</span> {{field.field_name|lower}} = document.<span class="js-function">querySelector</span>(<span class="js-body-str">'#{{field.field_name|lower}}'</span>).value;{% endif %}{% endfor %}

    <span class="js-keyword">const</span> data = {
        <span class="js-body-str">"tempId"</span>: <span>{{template_id}}</span>, <span class="js-body-com">// "tempId": 123,</span>{% for field in fields %}
        <span class="js-body-str">"{{field.field_name|lower}}"</span>: {{field.field_name|lower}},{% endfor %}
    };

    <span class="js-keyword">let</span> response = <span class="js-keyword">await</span> <span class="js-function">fetch</span>(<span class="js-body-str">'{{domain}}/api/send_data/'</span>, {
        method: <span class="js-body-str">'POST'</span>,
        headers: {
            <span class="js-body-str">'Content-Type'</span>: <span class="js-body-str">'application/json'</span>,
            <span class="js-body-str">'Authorization'</span>: <span class="js-body-str">'Token ' + 'Ваш_токен'</span>
        },
        body: JSON.<span class="js-function">stringify</span>(data),
      });
    <span class="js-keyword">let</span> result = <span class="js-keyword">await</span> response.<span class="js-function">json()</span>;
    console.<span class="js-function">log</span>(result);
};
                </code>
            </pre>""")

        js_code = js_template.render(fields=fields, template_id=template_id, domain=domain)
        return js_code

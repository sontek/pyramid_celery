<html>
  <body>
    <fieldset>
      % if tasks:
          <legend>Tasks</legend>
        % for task in tasks:
          Task: ${task.task}<a href="${request.route_url('delete_task', task_pk=task.id)}"> [ delete ] </a><br />
        % endfor
      % else:
        No tasks
      % endif
    </fieldset>
    <br />
    <form action="/add_task" method="POST">
        Add More:
        <input name="task" />
        <button type="submit">Add</button>
    </form>
  </body>
</html>
